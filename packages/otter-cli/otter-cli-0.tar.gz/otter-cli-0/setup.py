import os
import re
import json
from setuptools import setup


kwargs = {
        'name': 'otter-cli',
        'version': '0',
        'description': 'Command line interface for interacting with Otter Web API',
        'packages': ['otter_cli'],
        'zip_safe': False,
        'scripts': ['scripts/otter'],
        }

setup(**kwargs)



