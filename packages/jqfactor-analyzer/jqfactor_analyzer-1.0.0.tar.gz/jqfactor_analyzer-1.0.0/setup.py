#!/usr/bin/env python
# coding:utf-8

from __future__ import print_function

from os.path import join as path_join, dirname as path_dirname

from setuptools import setup, find_packages

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


requirements = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]


def get_version():
    scope = {}
    with open(path_join(path_dirname(__file__), "jqfactor_analyzer", "version.py")) as fp:
        exec(fp.read(), scope)
    return scope.get('__version__', '1.0')


def get_long_description():
    with open(path_join(path_dirname(__file__), 'README.md'), 'rb') as fp:
        long_desc = fp.read().decode('utf-8')

    with open(path_join(path_dirname(__file__), 'docs', 'apis.md'), 'rb') as fp:
        apis_desc = fp.read().decode('utf-8')

    return "{}\n\n{}".format(long_desc.replace('docs/apis.md', ''), apis_desc)


setup_args = dict(
    name='jqfactor_analyzer',
    version=get_version(),
    packages=find_packages(exclude=("tests", "tests.*")),
    author='JoinQuant',
    author_email='xlx@joinquant.com',
    maintainer="",
    maintainer_email="",
    url='https://www.joinquant.com',
    description='JoinQuant single factor analyzer',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    platforms=["all"],
    license='Apache License v2',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=requirements,
)


def main():
    setup(**setup_args)


if __name__ == "__main__":
    main()
