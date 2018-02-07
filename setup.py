#!/usr/bin/env python3

from setuptools import setup

import llama


# Helper
def read_file(filename):
    with open(filename) as f:
        return f.read()


setup(name="llama-mqtt",
      version=llama.__version__,
      description="An opinionated library for writing MQTT services",
      author=llama.__author__,
      author_email=llama.__email__,
      url="https://github.com/cameliot/llama",
      long_description=read_file("README.md"),
      classifiers=[

      ],
      keywords=["mqtt", "actor", "react", "service"],
      license=llama.__license__,
      packages=["llama"],
      install_requires=["paho-mqtt"],
      python_requires=">=3",
)
