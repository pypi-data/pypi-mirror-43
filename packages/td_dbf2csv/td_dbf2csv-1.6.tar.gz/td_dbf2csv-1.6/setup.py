# coding: utf-8
from setuptools import setup, find_packages
from dbf2csv import __version__

setup(
    name='td_dbf2csv',
    version=__version__,
    url='https://github.com/calebdinsmore/dbf2csv',
    description='Small utility to convert simple *.DBF files to *.CSV',
    packages=find_packages(),
    platforms='any',
    entry_points={
        'console_scripts': [
            'td-dbf2csv = dbf2csv.main:main',
        ],
    },
    install_requires=[
        'td-dbfread',
        'future',
    ]
)
