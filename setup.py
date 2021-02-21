"""Minimal setup file for tasks project."""

from os import name
from setuptools import setup, find_packages


setup(
    name='tasks',
    version='0.2.1.dev3',
    license='proprietary',
    description='Minimal Projecy Task Manager',

    author='Brian Okken',
    author_email='Please use pythontesting.net contact form.',
    url='https://pragprog.com/book/bopytest',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[
        'click==7.1.2',
        'tinydb==3.15.1',
        'six',
        'pytest<5.0.0',
        'pytest-mock==3.2.0',
        'pymongo'
        ],
    extras_require={'mongo': 'pymongo'},

    entry_points={
        'console_scripts': [
            'tasks = tasks.cli:tasks_cli'
        ]
    },

    include_package_data=True,
)