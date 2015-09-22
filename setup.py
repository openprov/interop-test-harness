#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

requirements = [
    'pyyaml',
]

test_requirements = [
    'nose',
    'nose_parameterized',
]

setup(
    name='prov_interop',
    version='0.0.1',
    description='Provenance Tool Suite interoperability test harness framework',
    author='Mike Jackson',
    author_email='michaelj@epcc.ed.ac.uk',
    url='https://github.com/prov-suite/interop-test-harness',
    packages=find_packages(),
    package_dir={
        'prov_interop': 'prov_interop'
    },
    data_files=[('prov_interop/interop_tests', ['prov_interop/interop_tests/harness.yaml'])],
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License",
    zip_safe=False,
    keywords=[
        'provenance', 'graph', 'model', 'PROV', 'PROV-DM', 'PROV-JSON', 'JSON',
        'PROV-XML', 'PROV-N'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    test_suite='prov_interop.tests',
    tests_require=test_requirements
)
