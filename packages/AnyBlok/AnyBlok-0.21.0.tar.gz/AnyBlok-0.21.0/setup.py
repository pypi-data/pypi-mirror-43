#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for tools-kehl-sensee"""

from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(os.path.join(here, 'CHANGELOG.rst'), 'r', encoding='utf-8') as changelog_file:
    changelog = changelog_file.read()

with open(os.path.join(here, 'VERSION'), 'r', encoding='utf-8') as version_file:
    version = version_file.read().strip()

requirements = [
    'pika==0.12',
    'anyblok_bus',
    'bus_schema',
    'optical',
    'bloks_sensee'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='toolsapi',
    python_requires='>3.6',
    version=version,
    description="Tools api for sensee / lmc",
    long_description=readme + '\n\n' + changelog,
    author="Franck Bret",
    author_email='f.bret@sensee.com',
    url='https://lab.sensee/it/tools-khel-sensee',
    packages=find_packages(),
    entry_points={
        'anyblok.init': [
            'kehl_config=toolsapi:anyblok_init_config',
        ],
        'bloks': [
            'toolsapiblok=toolsapi.toolsapiblok:Toolsapiblok'
        ],
        'console_scripts': [
            ('convert_attachment_from_lb_to_lo=toolsapi.scripts:'
             'convert_attachment_from_lb_to_lo'),
            'import_inventory=toolsapi.scripts:import_inventory',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='tools-api_sensee',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
