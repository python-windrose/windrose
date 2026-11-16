"""Checks for the source distribution's project metadata."""

import tomllib
from pathlib import Path


def test_dependency_groups_are_lists():
    with (Path(__file__).parents[1] / "pyproject.toml").open("rb") as stream:
        metadata = tomllib.load(stream)

    for name, dependencies in metadata["dependency-groups"].items():
        assert isinstance(dependencies, list), name


def test_project_urls():
    with (Path(__file__).parents[1] / "pyproject.toml").open("rb") as stream:
        metadata = tomllib.load(stream)

    assert metadata["project"]["urls"] == {
        "documentation": "https://python-windrose.github.io/windrose",
        "homepage": "https://github.com/python-windrose/windrose",
        "repository": "https://github.com/python-windrose/windrose",
    }
