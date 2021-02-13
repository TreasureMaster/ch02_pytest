"""Minimal setup file for tasks project."""

from os import name
from setuptools import setup, find_packages


setup(
    name='tasks',
    version='0.1.4.dev2',
    license='proprietary',
    description='Minimal Projecy Task Manager',

    author='Brian Okken',
    author_email='Please use pythontesting.net contact form.',
    url='https://pragprog.com/book/bopytest',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['click==7.1.2', 'tinydb==3.15.1', 'six', 'pytest'],
    extras_require={'mongo': 'pymongo'},

    entry_points={
        'console_scripts': [
            'tasks = tasks.cli:tasks_cli'
        ]
    },

    include_package_data=True,
)