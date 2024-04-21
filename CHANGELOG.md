# Change Log

## Python Windrose

All notable changes to this code base will be documented in this file,
in every released version.

### Version 1.x.x (unreleased)

## What's Changed
* Fix issue where sometimes the plot sectors showed a straight line instead of a curved one (#137)

### Version 1.7.0

## What's Changed
* fix typo in docs for map overlay by @weber-s in https://github.com/python-windrose/windrose/pull/144
* Docs simplify map overlay by @weber-s in https://github.com/python-windrose/windrose/pull/145
* Fix variable calling/returning order by @sspagnol in https://github.com/python-windrose/windrose/pull/156
* Fix clean method in case var is nan. by @15b3 in https://github.com/python-windrose/windrose/pull/164
* Fix default behavior of WindroseAxes.from_ax(). by @15b3 in https://github.com/python-windrose/windrose/pull/166
* Update docstring about calm_limit by @15b3 in https://github.com/python-windrose/windrose/pull/162
* fix np.float deprecation warning by @theendlessriver13 in https://github.com/python-windrose/windrose/pull/167
* move to GitHub Actions by @ocefpaf in https://github.com/python-windrose/windrose/pull/173
* Auto-publish on PyPI and test test the tarball by @ocefpaf in https://github.com/python-windrose/windrose/pull/174
* Build and upload docs by @ocefpaf in https://github.com/python-windrose/windrose/pull/175
* Codespell by @ocefpaf in https://github.com/python-windrose/windrose/pull/176
* Fix docs gha by @ocefpaf in https://github.com/python-windrose/windrose/pull/177
* Package metadata by @ocefpaf in https://github.com/python-windrose/windrose/pull/178
* Add pre-commit and many automated fixes by @ocefpaf in https://github.com/python-windrose/windrose/pull/179
* Add binder environment and badge by @ocefpaf in https://github.com/python-windrose/windrose/pull/180
* We no longer support Python 2k, so no universal wheel by @ocefpaf in https://github.com/python-windrose/windrose/pull/181

## New Contributors
* @sspagnol made their first contribution in https://github.com/python-windrose/windrose/pull/156
* @15b3 made their first contribution in https://github.com/python-windrose/windrose/pull/164
* @theendlessriver13 made their first contribution in https://github.com/python-windrose/windrose/pull/167

**Full Changelog**: https://github.com/python-windrose/windrose/compare/v1.6.8...v1.7.0

### Version 1.6.8

- Released: 2020-09-04
- Issues/Enhancements:
  - add custom units to the legend #128
- Fix:
  - Fix deprecated `_autogen_docstring` for matplotlib >3.1 (#136, #117, #119, #135)

### Version 1.6.7

- Released: 2019-06-07
- Issues/Enhancements:
  - Update release procedure for manual Pypi upload

### Version 1.6.6

- Released: 2019-06-07
- Issues/Enhancements:
  - Issue #81 #31 (PR #114) Remove use of pylab.poly_between
  - Calm conditions
  - Update CONTRIBUTORS.md and CONTRIBUTING.md
  - PR #107 Code formatting with Black
  - PR #104  Fix setup.py
  - Autodeploy to PyPI using Travis
  - PEP8

### Version 1.6.5

- Released: 2018-08-30
- Issues/Enhancements:
  - Issue #99. Fix scatter plot direction

### Version 1.6.4

- Released: 2018-08-22
- Issues/Enhancements:
  - Improve doc

### Version 1.6.3

- Released: 2017-08-22
- Issues/Enhancements:
  - Issue #69 (PR #70). Dual licensing
  - ...

### Version 1.6.2

- Released: 2017-08-02
- Issues/Enhancements:
  - Issue #65 (PR #69). Fix inconsistent licence files
  - ...

### Version 1.6.1

- Released: 2017-07-30
- Maintainer: Sébastien Celles <s.celles@gmail.com>
- Issues/Enhancements:
  - Original code forked from http://youarealegend.blogspot.fr/search/label/windrose
  - Create a pip instalable package (registered)
  - ...

### Version 1.5.0

- Initial development: 2015-06-16
- Co-Authors:
  - Sébastien Celles <s.celles@gmail.com>
  - Lionel Roubeyrie <lionel.roubeyrie@gmail.com>
- Maintainer: Sébastien Celles <s.celles@gmail.com>
- Issues/Enhancements:
  - Github repository creation
  - Create a package
  - Add unit tests / continuous integration
  - Pandas DataFrames / Series as input (keeping Numpy Array compatibility)
  - Python 2.7/3.x support
  - PDF output
  - Animate windrose (video output)
  - Add unit tests / continuous integration
  - PEP8
  - Register projection windrose
  - Weitbul plot


### Version 1.4.0

- Author: Lionel Roubeyrie <lionel.roubeyrie@gmail.com>
- URL: http://youarealegend.blogspot.fr/search/label/windrose
