import os
import sys

from pprint import pprint
from setuptools import setup, find_packages
# from spira.settings import __version__, __release__

sys.dont_write_bytecode = True


# packages = [
#     'spira',
#     'spira.core',
#     'technologies',
#     'validatex',
#     'inductex',
#     'josim',
# ]


# def list_folders(root):
#     acc = []
#     for f in os.listdir(root):
#         if f != '_tests':
#             full_name = os.path.join(root, f)
#             if os.path.isdir(full_name):
#                 acc.append(full_name)
#                 acc += list_folders(full_name)
#     return acc


# # package_dir = {}
# # for p in packages:
# #     root = os.path.join('qeda', p)
# #     package_dir[p] = root
# #     subpackages = list_folders(root)
# #     for s in subpackages:
# #         name = s.replace(os.sep, '.')
# #         if name.startswith('qeda.'):
# #             name = name.replace('qeda.', '', 1)
# #         package_dir[name] = s

        
# package_dir = {}
# for p in packages:
#     root = os.path.join('spira', p)
#     package_dir[p] = root
#     subpackages = list_folders(root)
#     for s in subpackages:
#         name = s.replace(os.sep, '.')
#         if name.startswith('spira.'):
#             name = name.replace('spira.', '', 1)
#         package_dir[name] = s


# setup(
#     # name='SPiRA',
#     name='spira',
#     # version='{}-{}'.format(__version__, __release__),
#     version='{}-{}'.format('0.1.0', 'Auron [Beta]'),
#     description='Superconducting Circuit Modeling and Verification',
#     author='Ruben van Staden',
#     author_email='rubenvanstaden@gmail.com',
#     setup_requires=['setuptools-markdown'],
#     license='MIT',
#     url='https://github.com/rubenvanstaden/spira',
#     extra_path='qeda',
#     packages=package_dir.keys(),
#     # package_dir={'qeda': 'spira'},
#     # package_dir=package_dir,
#     package_dir={'': 'qeda'},
#     data_files=[('qeda', ['LICENSE',]),]
# )





packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
print(packages)




setup(
    name="spira",
    # version='{}-{}'.format(__version__, __release__),
    version='{}-{}'.format('0.1.0', 'Auron [Beta]'),
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
