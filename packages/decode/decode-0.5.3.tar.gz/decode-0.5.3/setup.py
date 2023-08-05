# coding: utf-8

"DESHIMA Code for data analysis"

# standard library
from setuptools import setup

# module constants
INSTALL_REQUIRES = [
    'numpy',
    'scipy',
    'astropy',
    'xarray',
    'matplotlib',
    'scikit-learn',
    'pyyaml',
    'tqdm',
]

PACKAGES = [
    'decode',
    'decode.core',
    'decode.core.array',
    'decode.core.cube',
    'decode.io',
    'decode.logging',
    'decode.plot',
    'decode.models',
    'decode.joke',
    'decode.utils',
    'decode.utils.misc',
    'decode.utils.ndarray'
]



# main
setup(
    name = 'decode',
    description = __doc__,
    version = '0.5.3',
    author = 'DESHIMA software team',
    author_email = 'tishida@ioa.s.u-tokyo.ac.jp',
    url = 'https://github.com/deshima-dev/decode',
    install_requires = INSTALL_REQUIRES,
    packages = PACKAGES,
    package_data = {'decode': ['data/*.yaml']},
)
