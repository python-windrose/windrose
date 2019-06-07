# Release procedure

## Python versions

* Ensure supported Python versions in `setup.py` and `.travis.yml` are corrects 

* Ensure windrose version is up to date in `version.py`

## CHANGELOG

* Ensure `CHANGELOG.md` have been updated

## Tag

* Tag commit and push to github

using Github website

Go to https://github.com/python-windrose/windrose/releases/new
tag: vx.x.x

or using cli

```bash
git tag -a x.x.x -m 'Version x.x.x'
git push windrose master --tags
```

* Verify on Zenodo

Go to https://zenodo.org/account/settings/github/repository/python-windrose/windrose

to ensure that new release have a DOI

## Upload to PyPI

### Automatic PyPI upload

PyPI deployment was set using https://docs.travis-ci.com/user/deployment/pypi/

When tagging a new release on Github, package should be automatically uploaded on PyPI.

### Manual PyPI upload

Ensure a `~/.pypirc` exists

```
[distutils] # this tells distutils what package indexes you can push to
index-servers = pypi
    pypi # the live PyPI
    pypitest # test PyPI

[pypi]
repository:http://pypi.python.org/pypi
username:scls
password:**********
```

Upload

```
git clean -xfd
python setup.py register sdist bdist_wheel --universal
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Verify on PyPI

Go to https://pypi.python.org/pypi/windrose/
or https://pypi.python.org/pypi?%3Aaction=pkg_edit&name=windrose
