#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='modelfeast',
    version='0.1.5',
    description=(
        'Pytorch model zoo'
    ),
    long_description='Pytorch model zoo for human, include all kinds of 2D CNN, 3D CNN, and CRNN',
    author='Chengyao Zheng',
    author_email='daili0015@gmail.com',
    maintainer='Chengyao Zheng',
    maintainer_email='daili0015@gmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/daili0015/ModelFeast',
    install_requires = [
    'torch>=0.4.0',
    'numpy>=1.10.0',
    ],
    classifiers=(
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5"
    ),

)
