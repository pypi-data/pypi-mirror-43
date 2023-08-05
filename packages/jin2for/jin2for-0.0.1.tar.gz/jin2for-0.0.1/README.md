# jin2for - Generate FORTRAN source files from jinja2 templates

[![pipeline status](https://gitlab.com/fverdugo/jin2for/badges/master/pipeline.svg)](https://gitlab.com/fverdugo/jin2for/commits/master)
[![coverage report](https://gitlab.com/fverdugo/jin2for/badges/master/coverage.svg)](https://gitlab.com/fverdugo/jin2for/commits/master)

## Installation

```bash
$ pip install jin2for
```

## Usage

### Basic usage

```bash
$ jin2for file1.t90 file2.t90
```
This renders the jinja template files `file1.t90` and `file2.t90` into the FORTRAN source files `file1.90` and `file2.f90`

Files `file1.t90` and `file2.t90` can also include or import some other jinja templates that are located in a folder `folder/for/included/templates`
different from the current working directory. In this case, `jin2for` has to be informed as follows:

```bash
$ jin2for -I folder/for/included/templates file1.t90 file2.t90
```

### More advanced usage

For more advanced usage, see documentation

## Documentation

```bash
$ jin2for -h
```
