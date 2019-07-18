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
    description="Superconducting Circuit Modeling and Verification",
    author="Ruben van Staden",
    author_email="rubenvanstaden@gmail.com",
    setup_requires=['setuptools-markdown'],
    license="MIT",
    url="https://github.com/rubenvanstaden/spira",

    install_requires=[
        # # Developer packages
        # 'halo',
        # 'pytest',

        # Visual packages
        'sphinxcontrib-napoleon',
        'matplotlib',
        'plotly',
        'pyqt5',
        'lxml',

        # Core packages
        'termcolor',
        'colorama',
        'pandoc',
        'scipy',
        'numpy',
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
