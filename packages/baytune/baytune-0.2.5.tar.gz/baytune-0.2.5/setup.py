#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup


with open('README.md') as readme_file:
    readme = readme_file.read()


with open('HISTORY.md') as history_file:
    history = history_file.read()


install_requires = [
    'enum34>=1.1.6; python_version=="2.7"',
    'more-itertools<6; python_version=="2.7"',  # some upstream bug
    'numpy>=1.14.2',
    'scikit-learn>=0.19.1',
    'scipy>=1.0.1',
    'six>=1.0',
]


tests_require = [
    'mock>=2.0.0',
    'pytest>=3.4.2',
    'pytest-cov>=2.6.0',
]


setup_requires = [
    'pytest-runner>=2.11.1',
]


development_requires = [
    # general
    'bumpversion>=0.5.3',
    'pip>=9.0.1',
    'watchdog>=0.8.3',

    # docs
    'm2r>=0.2.0',
    'Sphinx>=1.7.1',
    'sphinx_rtd_theme>=0.2.4',

    # style check
    'flake8>=3.5.0',
    'isort>=4.3.4',

    # fix style issues
    'autoflake>=1.2',  # keep this after flake8 to avoid
    'autopep8>=1.3.5', # version incompatibilities with flake8

    # distribute on PyPI
    'twine>=1.10.0',
    'wheel>=0.30.0',

    # Advanced testing
    'tox>=2.9.1',
    'coverage>=4.5.1',
]


setup(
    author='MIT Data To AI Lab',
    author_email='dailabmit@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Bayesian Tuning and Bandits',
    extras_require={
        'dev': development_requires + tests_require,
        'test': tests_require,
    },
    install_requires=install_requires,
    license='MIT license',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='machine learning hyperparameters tuning classification',
    name='baytune',
    packages=find_packages(include=['btb', 'btb.*']),
    setup_requires=setup_requires,
    test_suite='tests',
    tests_require=tests_require,
    url='https://github.com/HDI-Project/BTB',
    version='0.2.5',
    zip_safe=False,
)
