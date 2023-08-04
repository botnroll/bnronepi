from setuptools import setup, find_packages

name = "onepi"
version = "0.1.0"
description = "Python library to interface with BotnRoll One A"
url = "https://github.com/ninopereira/bnronepi/tree/main/onepi"
author = "Nino Pereira"
author_email = "ninopereira.pt@gmail.com"
license = "MIT"
packages = ["onepi"]
classifiers = [
    "Development Status :: - Alpoha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

# Package dependencies
install_requires = ["spidev"]

setup(
    name=name,
    version=version,
    description=description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=install_requires,
)
