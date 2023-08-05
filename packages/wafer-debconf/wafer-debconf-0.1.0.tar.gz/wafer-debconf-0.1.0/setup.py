#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='wafer-debconf',
    version='0.1.0',
    description='Wafer extensions used by DebConf',
    author='DebConf Team',
    author_email='debconf-team@lists.debian.org',
    url='https://salsa.debian.org/debconf-team/public/website/wafer-debconf',
    packages=find_packages(),
    include_package_data=True,
)
