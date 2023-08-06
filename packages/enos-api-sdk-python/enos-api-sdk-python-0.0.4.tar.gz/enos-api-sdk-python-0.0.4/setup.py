# coding: utf8
# Author:xuyang.li
# Date:2018/11/20
"""
    Install to PIP
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enos-api-sdk-python",
    version="0.0.4",
    author="lihu.yang",
    author_email="lihu.yang@envision-digital.com",
    description="EnOS API SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EnvisionIot/enos-api-sdk-python.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyOpenSSL==18.0.0',
        'requests==2.12.4'
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
)
