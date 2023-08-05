#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools script file
"""

from setuptools import setup, find_packages

setup(
    name='corenlp-webclient',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    description="A client library for CoreNLP server's simple web API.",
    url='https://github.com/tanbro/corenlp-webclient',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    license='AGPLv3+',
    keywords='CoreNLP NLP',

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/corenlp_webclient/version.py',
    },
    setup_requires=[
        'pytest-runner',
        'setuptools_scm',
        'setuptools_scm_git_archive',
    ],

    install_requires=[
        'dataclasses;python_version<"3.7"',
        'dataclasses-jsonschema',
        'emoji-data',
        'requests',
    ],

    tests_require=[
        'pytest',
        'python-dotenv',
    ],
    test_suite='tests',

    python_requires='>=3.6',

    package_data={},

    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
