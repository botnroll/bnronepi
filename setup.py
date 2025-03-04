# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

name = "onepi"
version = "1.1.0"
description = "Python library to interface with Bot'n Roll One A+"
url = "https://github.com/botnroll/bnronepi"
author = "Bot'n Roll"
author_email = "botnroll@botnroll.com"
license = "MIT"
packages = find_packages()
py_modules = ["onepi.one"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
install_requires = ["spidev", "matplotlib", "rpi-lgpio", "setproctitle"]  # Package dependencies

setup(
    name=name,
    version=version,
    description=description,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=classifiers,
    packages=find_packages(),
    include_package_data=True,
    package_data={'onepi':['utils/*.png'],'onepi':['utils/*.json'], 'onepi':['diagnostics/*.png']},
    install_requires=install_requires,
)
