#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

requirements = [ ]

setup(
    author="F. Marmuse & R. Lucken",
    author_email='romain.lucken@lpp.polytechnique.fr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="global model",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description= '\n\n' ,
    include_package_data=True,
    keywords='global model',
    name='LPP0D',
    packages=find_packages(),
    setup_requires=setup_requirements,
    
    test_suite='tests',
    tests_require=test_requirements,
    url='https://hephaistos.lpp.polytechnique.fr/rhodecode/GIT_REPOSITORIES/LPP/LPP0D',
    version='0.1.1',
    zip_safe=False,
)
