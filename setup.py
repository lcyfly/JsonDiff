#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/20 15:53
# @Author : Louchengwang
# @File : setup.py
# @Dream: NO BUG

from setuptools import setup, find_packages
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

setup(
    name="jsonAssured",

    version="0.0.2",

    keywords=("pip", "jsonAssured", "jsonpath"),

    description="diff json data by jsonpath",

    long_description="json path generator, json diff",

    url="https://github.com/lcyfly/JsonDiff.git",

    author="lcy815",

    author_email="252624008@qq.com",

    packages=find_packages(),

    platforms="any",

    install_requires=["pyyaml", "jsonpath"],

    scripts=[],
    entry_points={
        'console_scripts': [
            'jsonAssured=jsonAssured.jsonDiff:main'
        ]
    },
)
