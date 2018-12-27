import os
import sys

from pprint import pprint
from setuptools import setup, find_packages

sys.dont_write_bytecode = True

setup(
    name="spira",
    version='0.0.2',
    description="Superconducting Circuit Modeling and Verification",
    author="Ruben van Staden",
    author_email="rubenvanstaden@gmail.com",
    setup_requires=['setuptools-markdown'],
    license="MIT",
    url="https://github.com/rubenvanstaden/spira",

    install_requires=[
        # Visual packages
        'matplotlib',
        'plotly',
        'pyqt5'
        'lxml',

        # Basic packages
        'termcolor',
        'colorama',
        'pandoc',
        'scipy',
        'pytest',

        # Core packages
        'gdspy',
        'shapely',
        'pyclipper',
        'networkx',
        'pygmsh',
        'meshio',
    ],

    packages=['spira',
              'spira.core',
              'spira.gdsii',
              'spira.lgm',
              'spira.lne',
              'spira.lpe',
              'spira.lrc',
              'spira.param',
              'spira.rdd'],

    package_dir={'spira': 'spira'}
)
