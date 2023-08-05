from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wtfix",
    version="0.1.0",
    author="John Cass",
    author_email="john.cass77@gmail.com",
    description="The Pythonic Financial Information eXchange client for humans.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jcass77/WTFIX",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    keywords="FIX financial information exchange",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["python-dotenv~=0.9", "unsync~=1.1"],
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/jcass77/WTFIX/issues",
        "Source": "https://github.com/jcass77/WTFIX/",
    },
)
