# This file is a part of WTFIX.
#
# Copyright (C) 2018,2019 John Cass <john.cass77@gmail.com>
#
# WTFIX is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# WTFIX is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aiofiles
import asyncio

import pytest

from wtfix.conf import settings
from wtfix.core import utils


class TestClientSessionApp:
    @pytest.mark.skip("TODO")
    @pytest.mark.asyncio
    async def test_listen(self):
        begin_string = b"8=" + utils.encode(settings.BEGIN_STRING)
        checksum_start = settings.SOH + b"10="

        async with aiofiles.open("sample_mdr_msg.txt", mode="rb") as f:
            contents = await f.read()

            reader = asyncio.StreamReader()
            reader.feed_data(contents)
            data = await reader.readuntil(begin_string)  # Detect beginning of message.
            data += await reader.readuntil(
                checksum_start
            )  # Detect start of checksum field.
            data += await reader.readuntil(
                settings.SOH
            )  # Detect final message delimiter.

        assert data == contents
        #     contents = await f.read()
        # print(contents)
        # 'My file contents'
