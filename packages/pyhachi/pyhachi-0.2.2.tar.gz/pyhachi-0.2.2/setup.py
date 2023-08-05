#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup, find_packages
import sys

if sys.version_info<(3,):
    sys.exit("Sorry, Python 3 is required for PyHachi")

with open("requirements.txt", "r") as f:
    reqs = [l for l in f.read().splitlines() if l]

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name="pyhachi",
    version="0.2.2",
    description="spam filter",
    long_description=long_description,
    author='Guokr Inc.',
    author_email='jinyang.zhou@guokr.com',
    # url="https://github.com/guokr/Caver",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
    ),
    entry_points={
        'console_scripts': [
            # 'trickster_train=trickster::train',
        ]
    },
    install_requires=reqs
)
