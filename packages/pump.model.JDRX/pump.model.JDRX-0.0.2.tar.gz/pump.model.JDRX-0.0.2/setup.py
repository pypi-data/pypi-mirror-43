#!/usr/bin/python35
# coding: utf-8


"""
@version: 1.0
@author: LiYuBao
@contact: LiYuBao@evercreative.com.cn
@site: http://www.evercreative.com.cn/
@software: PyCharm
@file: setup.py
@time: 2019/3/14 16:50
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pump.model.JDRX",
    version="0.0.2",
    author="JDRX_LiYuBao",
    author_email="author@example.com",
    description="Pump package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)