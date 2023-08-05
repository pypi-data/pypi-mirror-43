# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyscbwrapper",
    version="0.1",
    author="Kira Coder Gylling",
    author_email="kira.gylling@gmail.com",
    description="Wrapper for Statistics Sweden's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kirajcg/pyscbwrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
