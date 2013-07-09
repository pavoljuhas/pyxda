#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyxda - X-ray Data Analysis Library
"""

from setuptools import setup, find_packages

setup(name='pyxda.rawviewer',
      version='0.1',
      namespace_packages = ['pyxda'],
      packages = find_packages(),
      scripts = [],
      data_files = [],
      install_requires = [],
      dependency_links = [],
      entry_points = {
        'console_scripts': ['pyxda = pyxda.command_line:main', 
                            'pyxda--rawviewer=pyxda.rawviewer.uipyxda:main'],
      },
)