#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click', 'requests', 'pytz']

setup_requirements = []

test_requirements = ['vcrpy', ]

setup(
    name='badgr_lite',
    version='0.0.1',
    author="Glen Jarvis",
    author_email='glen@glenjarvis.com',
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Automate awarding Badgr (or equivalent) badges to recipients without the overhead of badgr-server",
    entry_points={
        'console_scripts': [
            'badgr=badgr_lite.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='OpenBadge',
    packages=find_packages(include=['badgr_lite', 'badgr_lite.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/glenjarvis/badgr_lite',
    zip_safe=False,
)
