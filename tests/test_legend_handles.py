"""Legend handles can be shared between windrose axes."""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from numpy.testing import assert_allclose

from windrose import WindroseAxes


@pytest.mark.parametrize("kind", ["bar", "box", "contour", "contourf"])
def test_get_legend_handles_labels(kind):
    fig = plt.figure()
    try:
        ax = WindroseAxes.from_ax(fig=fig)
        getattr(ax, kind)(
            np.linspace(0, 360, 20),
            np.linspace(0, 10, 20),
            bins=[0, 3, 6, 9],
        )
        handles, labels = ax.get_legend_handles_labels()
        assert labels == ["[0.0 : 3.0)", "[3.0 : 6.0)", "[6.0 : 9.0)", ">9.0"]
        assert len(handles) == 4
        assert ax.get_legend() is None
        for handle, patch in zip(handles, ax.patches_list, strict=True):
            color = (
                patch.get_color()
                if kind == "contour"
                else patch.get_facecolor()
            )
            assert_allclose(handle.get_facecolor(), color)
        legend = fig.legend(handles, labels, loc="lower center", ncols=4)
        assert [text.get_text() for text in legend.get_texts()] == labels
        fig.canvas.draw()
    finally:
        plt.close(fig)


def test_get_legend_handles_preserves_axes_legend():
    fig = plt.figure()
    try:
        ax = WindroseAxes.from_ax(fig=fig)
        ax.bar([0, 90, 180, 270], [1, 3, 5, 7], bins=[0, 4, 8])
        existing = ax.legend(decimal_places=2, units="m/s")
        handles, labels = ax.get_legend_handles_labels(
            decimal_places=2,
            units="m/s",
        )
        assert ax.get_legend() is existing
        assert labels == [text.get_text() for text in existing.get_texts()]
        assert len(handles) == 3
        ax.clear()
        assert ax.get_legend_handles_labels() == ([], [])
    finally:
        plt.close(fig)


def test_get_legend_handles_includes_labeled_artists():
    fig = plt.figure()
    try:
        ax = WindroseAxes.from_ax(fig=fig)
        (line,) = ax.plot([0, 1], [1, 2], label="reference")
        assert ax.get_legend_handles_labels() == ([line], ["reference"])
        ax.bar([0, 90, 180, 270], [1, 3, 5, 7], bins=[0, 4, 8])
        handles, labels = ax.get_legend_handles_labels()
        assert handles[-1] is line
        assert labels == ["[0.0 : 4.0)", "[4.0 : 8.0)", ">8.0", "reference"]
    finally:
        plt.close(fig)


def test_get_legend_handles_french_labels(monkeypatch):
    monkeypatch.setattr(
        "windrose.windrose.locale.getlocale",
        lambda: ("fr_FR", "UTF-8"),
    )
    fig = plt.figure()
    try:
        ax = WindroseAxes.from_ax(fig=fig)
        ax.bar([0, 90], [1, 5], bins=[0, 4, 8])
        _, labels = ax.get_legend_handles_labels()
        assert labels == ["[0.0 : 4.0[", "[4.0 : 8.0[", ">8.0"]
    finally:
        plt.close(fig)
