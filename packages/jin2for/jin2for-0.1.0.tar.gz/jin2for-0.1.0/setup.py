# This file is part of the jin2for project
# (c) 2019 Francesc Verdugo <fverdugo@cimne.upc.edu>

import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jin2for",
    version="0.1.0",
    author="Francesc Verdugo",
    author_email="fverdugo@cimne.upc.edu",
    description="A jinja2-based template engine for FORTRAN projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fverdugo/jin2for",
    py_modules = ['jin2for',],
    packages=['jin2for'],
    package_data={'jin2for': ['data/*.f90']},
    install_requires=['argparse','jinja2'],
    setup_requires=["pytest-runner",],
    tests_require=["pytest","pytest-cov"],
    entry_points = {'console_scripts':['jin2for=jin2for:main',]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Fortran",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS"
    ],
)
