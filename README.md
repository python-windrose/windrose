[![Latest Version](https://img.shields.io/pypi/v/windrose.svg)](https://pypi.python.org/pypi/windrose/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/windrose.svg)](https://pypi.python.org/pypi/windrose/)
[![Wheel format](https://img.shields.io/pypi/wheel/windrose.svg)](https://pypi.python.org/pypi/windrose/)
[![License](https://img.shields.io/pypi/l/windrose.svg)](https://pypi.python.org/pypi/windrose/)
[![Development Status](https://img.shields.io/pypi/status/windrose.svg)](https://pypi.python.org/pypi/windrose/)
[![Tests](https://github.com/python-windrose/windrose/actions/workflows/tests.yml/badge.svg)](https://github.com/python-windrose/windrose/actions/workflows/tests.yml)
[![DOI](https://zenodo.org/badge/37549137.svg)](https://zenodo.org/badge/latestdoi/37549137)
[![JOSS](https://joss.theoj.org/papers/10.21105/joss.00268/status.svg)](https://joss.theoj.org/papers/10.21105/joss.00268)

# Windrose

A [wind rose](https://en.wikipedia.org/wiki/Wind_rose) is a graphic tool used by meteorologists to give a succinct view of how wind speed and direction are typically distributed at a particular location. It can also be used to describe air quality pollution sources. The wind rose tool uses Matplotlib as a backend. Data can be passed to the package using Numpy arrays or a Pandas DataFrame.

Windrose is a Python library to manage wind data, draw windroses (also known as polar rose plots), and fit Weibull probability density functions.

The initial use case of this library was for a technical report concerning pollution exposure and wind distributions analyzes. Data from local pollution measures and meteorologic information from various sources like Meteo-France were used to generate a pollution source wind rose.

It is also used by some contributors for teaching purpose.

![Map overlay](paper/screenshots/overlay.png)

Some others contributors have used it to make figures for a [wind power plant control optimization study](https://www.nrel.gov/docs/fy17osti/68185.pdf).

Some academics use it to track lightning strikes during high intensity storms. They are using it to visualize the motion of storms based on the relative position of the lightning from one strike to the next.

## Try windrose on mybinder.org

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/python-windrose/windrose/HEAD?labpath=notebooks)

## Install

### Requirements

- matplotlib http://matplotlib.org/
- numpy http://www.numpy.org/
- and naturally python https://www.python.org/ :-P

Option libraries:

- Pandas http://pandas.pydata.org/ (to feed plot functions easily)
- Scipy http://www.scipy.org/ (to fit data with Weibull distribution)
- ffmpeg https://www.ffmpeg.org/ (to output video)
- click http://click.pocoo.org/ (for command line interface tools)

### Install latest release version via pip

A package is available and can be downloaded from PyPi and installed using:

```bash
$ pip install windrose
```

### Install latest development version

```bash
$ pip install git+https://github.com/python-windrose/windrose
```

or

```bash
$ git clone https://github.com/python-windrose/windrose
$ python setup.py install
```

## Documentation
Full documentation of library is available at https://python-windrose.github.io/windrose/

## Community guidelines

You can help to develop this library.

### Code of Conduct

If you are using Python Windrose and want to interact with developers, others users...
we encourage you to follow our [code of conduct](https://github.com/python-windrose/windrose/blob/master/CODE_OF_CONDUCT.md).

### Contributing

If you discover issues, have ideas for improvements or new features, please report them.
[CONTRIBUTING.md](https://github.com/python-windrose/windrose/blob/master/CONTRIBUTING.md) explains
how to contribute to this project.

### List of contributors and/or notable users
https://github.com/python-windrose/windrose/blob/master/CONTRIBUTORS.md
