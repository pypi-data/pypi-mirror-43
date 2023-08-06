# -*- coding: utf-8 -*-
"""
python setup.py sdist upload -r pypi
"""

from setuptools import setup, find_packages
from stallions import __version__

VERSION = __version__

readability_lxml = "readability-lxml"

setup(
    name='stallions',
    version=VERSION,
    description='Extract the content of the web page.',
    license='',
    author='galen',
    author_email='galen.wang@rtbasia.com',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://git.rtbasia.com/galen/python_stallion',
    keywords='Web spider',
    packages=find_packages(),
    install_requires=[
        readability_lxml,
        'lxml',
        'requests',
    ],
)
