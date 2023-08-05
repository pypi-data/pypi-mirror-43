#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "kdLaunchPad",
    version = "1.0.0",
    keywords = ("pip", "kdLaunchPad","autoStarter"),
    description = "auto run some programs after system start",
    long_description = "configure some programs as a session,and start them after the system startup.",
    license = "GPL Licence",

    url = "https://github.com/bkdwei/kdLaunchPad",
    author = "bkdwei",
    author_email = "bkdwei@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["PyQt5"]
)