import asyncio
from unittest import mock
from unittest.mock import MagicMock

import pytest
from unsync import Unfuture

from wtfix.apps.admin import HeartbeatApp, SeqNumManagerApp
from wtfix.core.exceptions import MessageProcessingError, StopMessageProcessing
from wtfix.message import admin
from wtfix.message.admin import TestRequestMessage, HeartbeatMessage
from wtfix.pipeline import BasePipeline
from wtfix.protocol.common import Tag


class TestHeartbeatApp:
    def test_heartbeat_getter_defaults_to_30(self):
        heartbeat_app = HeartbeatApp(MagicMock(BasePipeline))
        assert heartbeat_app.heartbeat == 30

    @pytest.mark.asyncio
    async def test_server_stops_responding_after_three_test_requests(
        self, unsync_event_loop, failing_server_heartbeat_app
    ):
        await failing_server_heartbeat_app.monitor_heartbeat()

        assert failing_server_heartbeat_app.pipeline.send.call_count == 4
        assert failing_server_heartbeat_app.pipeline.stop.called

    @pytest.mark.asyncio
    async def test_monitor_heartbeat_test_request_not_necessary(
        self, unsync_event_loop, zero_heartbeat_app
    ):
        """Simulate normal heartbeat rhythm - message just received"""
        with mock.patch.object(
            HeartbeatApp, "send_test_request", return_value=Unfuture.from_value(None)
        ) as check:

            zero_heartbeat_app.sec_since_last_receive.return_value = 0
            try:
                await asyncio.wait_for(zero_heartbeat_app.monitor_heartbeat(), 0.1)
            except asyncio.futures.TimeoutError:
                pass

            assert check.call_count == 0

    @pytest.mark.asyncio
    async def test_monitor_heartbeat_heartbeat_exceeded(
        self, unsync_event_loop, zero_heartbeat_app
    ):
        """Simulate normal heartbeat rhythm - heartbeat exceeded since last message was received"""
        with mock.patch.object(
            HeartbeatApp, "send_test_request", return_value=Unfuture.from_value(None)
        ) as check:

            try:
                await asyncio.wait_for(zero_heartbeat_app.monitor_heartbeat(), 0.1)
            except asyncio.futures.TimeoutError:
                pass

            assert check.call_count > 1

    @pytest.mark.asyncio
    async def test_send_test_request(self, unsync_event_loop, zero_heartbeat_app):
        def simulate_heartbeat_response(message):
            zero_heartbeat_app.on_heartbeat(
                {Tag.TestReqID: message[Tag.TestReqID].as_str}
            )

        zero_heartbeat_app.pipeline.send.side_effect = simulate_heartbeat_response

        try:
            await asyncio.wait_for(zero_heartbeat_app.monitor_heartbeat(), 0.1)
        except asyncio.futures.TimeoutError:
            pass

        assert not zero_heartbeat_app._server_not_responding.is_set()

    @pytest.mark.asyncio
    async def test_send_test_request_no_response(
        self, unsync_event_loop, zero_heartbeat_app
    ):
        await zero_heartbeat_app.send_test_request()
        assert zero_heartbeat_app._server_not_responding.is_set()

    def test_logon_sets_heartbeat_increment(self, logon_message):
        heartbeat_app = HeartbeatApp(MagicMock(BasePipeline))

        logon_message[Tag.HeartBtInt] = 45
        heartbeat_app.on_logon(logon_message)

        assert heartbeat_app.heartbeat == 45

    def test_sends_heartbeat_on_test_request(self, zero_heartbeat_app):
        request_message = TestRequestMessage("test123")
        zero_heartbeat_app.on_test_request(request_message)

        zero_heartbeat_app.pipeline.send.assert_called_with(
            admin.HeartbeatMessage("test123")
        )

    def test_resets_request_id_when_heartbeat_received(self, zero_heartbeat_app):
        heartbeat_message = HeartbeatMessage("test123")
        zero_heartbeat_app._test_request_id = "test123"

        zero_heartbeat_app.on_heartbeat(heartbeat_message)

        assert zero_heartbeat_app._test_request_id is None

    def test_raises_exception_on_unexpected_heartbeat(self, zero_heartbeat_app):
        with pytest.raises(MessageProcessingError):
            heartbeat_message = HeartbeatMessage("123test")
            zero_heartbeat_app._test_request_id = "test123"

            zero_heartbeat_app.on_heartbeat(heartbeat_message)

    def test_on_receive_updated_timestamp(self, zero_heartbeat_app):
        prev_timestamp = zero_heartbeat_app._last_receive

        zero_heartbeat_app.on_receive(TestRequestMessage("test123"))
        assert zero_heartbeat_app._last_receive != prev_timestamp


class TestSeqNumManagerApp:
    def test_on_resend_request_sends_resend_request(self, messages):
        pipeline_mock = MagicMock(BasePipeline)
        seq_num_app = SeqNumManagerApp(pipeline_mock)

        seq_num_app._send_log = {message.seq_num: message for message in messages}
        seq_num_app._send_seq_num = max(seq_num_app._send_log.keys())

        resend_begin_seq_num = 2

        seq_num_app.on_resend_request(admin.ResendRequestMessage(resend_begin_seq_num))

        assert pipeline_mock.send.call_count == 4

        for idx in range(pipeline_mock.send.call_count):
            message = pipeline_mock.send.mock_calls[idx][1][0]
            # Check sequence number
            assert message.seq_num == resend_begin_seq_num + idx
            # Check PossDup flag
            assert message.PossDupFlag.as_bool is True
            # Check sending time
            assert message.OrigSendingTime.value_ref == message.SendingTime.value_ref

    def test_on_resend_request_handles_admin_messages_correctly(
        self, logon_message, messages
    ):
        pipeline_mock = MagicMock(BasePipeline)
        seq_num_app = SeqNumManagerApp(pipeline_mock)

        admin_messages = [logon_message, HeartbeatMessage("test123")]

        # Inject admin messages
        messages = admin_messages + messages

        # Reset sequence numbers
        for idx, message in enumerate(messages):
            message.MsgSeqNum = idx + 1

        seq_num_app._send_log = {message.seq_num: message for message in messages}
        seq_num_app._send_seq_num = max(seq_num_app._send_log.keys())

        resend_begin_seq_num = 1

        seq_num_app.on_resend_request(admin.ResendRequestMessage(resend_begin_seq_num))

        assert pipeline_mock.send.call_count == 6

        admin_messages_resend = pipeline_mock.send.mock_calls[0][1][0]
        # Check SequenceReset message is constructed correctly
        assert admin_messages_resend.seq_num == 1
        assert admin_messages_resend.NewSeqNo.as_int == 3
        assert admin_messages_resend.PossDupFlag.as_bool is True

        # Check first non-admin message starts with correct sequence number
        first_non_admin_message_resend = pipeline_mock.send.mock_calls[1][1][0]
        assert first_non_admin_message_resend.seq_num == 3

    def test_on_receive_no_gaps_adds_messages_to_receive_log(self, messages):
        seq_num_app = SeqNumManagerApp(MagicMock(BasePipeline))

        for next_message in messages:
            seq_num_app.on_receive(next_message)

        assert seq_num_app.receive_seq_num == 5
        assert seq_num_app.expected_seq_num == 6

        assert all(
            message.MsgSeqNum.as_int in seq_num_app._receive_log.keys()
            for message in messages
        )

    def test_on_receive_with_gaps_sends_resend_request(self, messages):
        pipeline_mock = MagicMock(BasePipeline)
        seq_num_app = SeqNumManagerApp(pipeline_mock)

        seq_num_app.on_receive(messages[0])

        try:
            seq_num_app.on_receive(messages[-1])
            assert False  # Should not reach here
        except StopMessageProcessing:
            # Expected - ignore
            pass

        assert pipeline_mock.send.call_count == 1

    def test_on_receive_ignores_poss_dups(self, messages):
        pipeline_mock = MagicMock(BasePipeline)
        seq_num_app = SeqNumManagerApp(pipeline_mock)

        for next_message in messages:
            seq_num_app.on_receive(next_message)

        try:
            dup_message = messages[-1]
            dup_message.PossDupFlag = "Y"
            seq_num_app.on_receive(dup_message)

            assert False  # Should not reach here
        except StopMessageProcessing:
            # Expected - ignore
            pass
