#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name = "kdPythonAPIViewer",
    version = "1.0.4",
    keywords = ( "kdPythonAPIViewer","API viewer"),
    description = "view API doc",
    long_description = "query API doc ,query the module method and attribute",
    license = "GPLv3+",

    url = "https://github.com/bkdwei/kdPythonAPIViewer",
    author = "bkdwei",
    author_email = "bkdwei@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["PyQt5"]
)
