"""
Douban Photo Dowloader
"""

from setuptools import setup, find_packages

requirements = [
    'bs4',
    'requests'
]

def long_desc():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name = 'lilyzt-douban-dl',
    version = '1.0.0',
    description = 'Douban Photo Downloader',
    long_description = long_desc(),
    url = 'https://gitlab.com/hxlhxl2012/douban-dl',
    author = 'hxlhxl2012',
    licence = 'MIT',
    keywords = 'douban downloader',
    packages= find_packages(exclude = ['tests']),
    install_requires = requirements,
    entry_points = {
        'console_scripts': [
            'lilyzt-douban-dl = douban:main',
        ]
    },
)
