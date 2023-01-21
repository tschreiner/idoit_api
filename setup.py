#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Tedd Schreiner",
    author_email='info@teddschreiner.de',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="i-doit API Client for Python. Translated from the original PHP source.",
    entry_points={
        'console_scripts': [
            'idoit_api_client=idoit_api_client.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description='',
    include_package_data=True,
    keywords='idoit_api_client',
    name='idoit_api_client',
    packages=find_packages(include=['idoit_api_client', 'idoit_api_client.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tschreiner/idoit_api',
    version='0.0.2',
    zip_safe=False,
)
