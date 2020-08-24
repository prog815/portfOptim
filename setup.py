from setuptools import setup, find_packages
from os.path import join, dirname

import lib

setup(
    name='portfOptim',
    version='0.0.1',
    description='Библиотека оптимизации финансовых портфелей',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    author_email='eavprog@gmail.com'
)
