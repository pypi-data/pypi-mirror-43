from distutils.core import setup

from setuptools import find_packages

setup(
    name='gconf',
    version='0.5.2',
    packages=find_packages(),
    install_requires=[
        'pyyaml'
    ],
    extras_require={
        'dev': ['pytest']
    },
    url='https://gitlab.com/max-tet/gconf',
    license='LICENSE',
    author='Max von Tettenborn',
    author_email='max@vtettenborn.net',
    description='Managing a config globally throughout a Python application'
)
