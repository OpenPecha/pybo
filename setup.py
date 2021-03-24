#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import re
from pathlib import Path

import setuptools
from pkg_resources import parse_version

assert parse_version(setuptools.__version__) >= parse_version("38.6.0")


def get_version(prop, project):
    project = Path(__file__).parent / project / "__init__.py"
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), project.read_text()
    )
    return result.group(1)


def read(fname):
    p = Path(__file__).parent / fname
    with p.open(encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="pybo",
    version=get_version("__version__", "pybo"),  # edit version in pybo/__init__.py
    author="Esukhia development team",
    author_email="esukhiadev@gmail.com",
    description="Python utils for processing Tibetan",
    license="Apache2",
    keywords="nlp computational_linguistics search ngrams language_models linguistics toolkit tibetan",
    url="https://github.com/Esukhia/pybo",
    packages=setuptools.find_packages(),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/Esukhia/pybo",
        "Tracker": "https://github.com/Esukhia/pybo/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Tibetan",
    ],
    python_requires=">=3.6",
    install_requires=["botok>=0.8.2", "pyyaml", "click", "pyewts", "bordr", "tibetan_sort", "pytest"],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["bo=pybo.cli:cli"]  # command=package.module:function
    },
)
