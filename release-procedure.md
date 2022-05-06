# Release procedure

## Python versions

* ECheck `python_requires = >=3.6` in setup.cfg

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

PyPI deployment is done via https://github.com/python-windrose/windrose/blob/master/.github/workflows/publish.yml

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
python -m build --sdist --wheel . --outdir dist
python -m twine check dist/*
python -m twine upload dist/*
```

## Verify on PyPI

Go to https://pypi.org/project/windrose/
