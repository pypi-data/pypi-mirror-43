import os
import re
import json
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='otter-cli',
        version='0.0.1',
        description='Command line interface for interacting with Otter Web API',
        long_description=long_description,
        packages=['otter_cli'],
        zip_safe=False,
        scripts=['scripts/otter'],
        )




