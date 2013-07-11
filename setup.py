#!/usr/bin/env python
# coding=utf-8

"""pyxda - X-ray Data Analysis Library
"""

from setuptools import setup, find_packages

# define distribution
setup(
        name = "pyxda",
        version = "1.0",
        packages = find_packages(),
        package_data = {"pyxda" : ['tests/testdata/*']},
        author = 'Simon J.L. Billinge',
        author_email = 'sb2896@columbia.edu',
        maintainer = 'Pavol Juhas',
        maintainer_email = 'pavol.juhas@gmail.com',
        # url = '',
        # download_url = 'FIXME to github URL',
        description = "X-ray Data Analysis Library",
        license = 'BSD',
        classifiers = [
            # List of possible values at
            # http://pypi.python.org/pypi?:action=list_classifiers
            'Development Status :: 1 - Planning',
            'Intended Audience :: Science/Research',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics',
        ],
        entry_points = {
          'console_scripts': ['pyxda = pyxda.commandline:main', 
                              'rawviewer = pyxda.rawviewer.userinterface:main'],
      },
)
