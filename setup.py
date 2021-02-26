#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

from pathlib import Path
import setuptools
from pkg_resources import parse_version
import re

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
    package_data={"pybo": ["third_party/*", "resources/*"]},
    python_requires=">=3.6",
    dependency_links=[
        # pyicu for Windows
        "https://download.lfd.uci.edu/pythonlibs/g5apjq5m/PyICU-2.3.1-cp38-cp38-win_amd64.whl",
        "https://download.lfd.uci.edu/pythonlibs/g5apjq5m/PyICU-2.3.1-cp38-cp38-win32.whl",
        "https://download.lfd.uci.edu/pythonlibs/g5apjq5m/PyICU-2.3.1-cp37-cp37m-win_amd64.whl",
        "https://download.lfd.uci.edu/pythonlibs/g5apjq5m/PyICU-2.3.1-cp37-cp37m-win32.whl",
        "https://download.lfd.uci.edu/pythonlibs/g5apjq5m/PyICU-2.3.1-cp36-cp36m-win_amd64.whl",
        "https://download.lfd.uci.edu/pythonlibs/g5apjq5m/PyICU-2.3.1-cp36-cp36m-win32.whl",
    ],
    install_requires=["pyyaml", "click", "botok", "pyewts", "bordr"],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["pybo=pybo.cli:cli"]  # command=package.module:function
    },
)
