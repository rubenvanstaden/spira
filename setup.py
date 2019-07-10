import os
import sys

from pprint import pprint
from setuptools import setup, find_packages
from spira.settings import __version__, __release__

sys.dont_write_bytecode = True

packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

setup(
    name="spira",
    version='{}-{}'.format(__version__, __release__),
    # version='{}-{}'.format('0.1.0', 'Auron [Beta]'),
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
        'pyqt5',
        'lxml',

        # Developer packages
        'sphinxcontrib-napoleon',
        'halo',
        'pytest',

        # Basic packages
        'termcolor',
        'colorama',
        'pandoc',
        'scipy',
        'numpy',

        # Core packages
        'gdspy',
        'shapely',
        'pyclipper',
        'networkx',
        'pygmsh',
        'meshio',
    ],

    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    # packages=['spira',
    #           'spira.core',
    #           'spira',
    #           'spira.validatex',
    #           'spira.inductex',
    #           'spira.josim',
    # ],

    # package_dir={'spira': 'spira'}
)
