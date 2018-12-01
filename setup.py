import os
import sys

from pprint import pprint
from setuptools import setup, find_packages

sys.dont_write_bytecode = True

setup(
    name="spira",
    version='0.0.3',
    description="Superconducting Circuit Modeling and Verification",
    author="Ruben van Staden",
    author_email="rubenvanstaden@gmail.com",
    setup_requires=['setuptools-markdown'],
    license="MIT",
    url="https://github.com/rubenvanstaden/spira",

    install_requires=[
        'gdspy',
        'holoviews',
        'lxml',
        'shapely',
        'termcolor',
        'pyclipper',
        'colorama',
        'matplotlib',
        'networkx',
        'docopt',
        'pygmsh',
        'meshio',
        'pandoc',
        'scipy',
        'plotly',
        'pytest',
        'pyqt5'
    ],

    packages=['spira',
              'spira.kernel',
              'spira.lgm',
              'spira.lne',
              'spira.lpe',
              'spira.lrc',
              'spira.rdd',
              'spira.rdd',
              'spira.templates',
              'spira.routing'],

    package_dir={'spira': 'spira'}
)
