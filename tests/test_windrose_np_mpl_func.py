# generate the baseline: pytest tests/test_windrose_np_mpl_func.py --mpl-generate-path=tests/output/func

import matplotlib
import numpy as np
import pytest
from matplotlib import cm as cm

from windrose import wrbar, wrbox, wrcontour, wrcontourf, wrpdf, wrscatter

np.random.seed(0)

matplotlib.use("Agg")  # noqa
# Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360
bins = np.arange(0, 8, 1)


@pytest.mark.mpl_image_compare(baseline_dir="output/func", tolerance=10)
def test_wrscatter():
    ax = wrscatter(wd, ws, alpha=0.2)
    return ax.figure


def test_wrscatter_direction_convention():
    # 0 degrees is North (up) and angles increase clockwise, as for the
    # bar/box/contour plots: theta = radians(90 - direction).  See gh-99.
    compass = np.array([0.0, 45.0, 90.0, 180.0, 270.0])
    ax = wrscatter(compass, np.full_like(compass, 10.0))
    theta = ax.collections[0].get_offsets()[:, 0]
    two_pi = 2 * np.pi
    np.testing.assert_allclose(
        np.mod(theta, two_pi),
        np.mod(np.radians(90.0 - compass), two_pi),
    )


@pytest.mark.mpl_image_compare(baseline_dir="output/func", tolerance=5)
def test_wrbar():
    ax = wrbar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func", tolerance=20)
def test_wrbox():
    ax = wrbox(wd, ws, bins=bins)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func", tolerance=20)
def test_wrcontourf():
    ax = wrcontourf(wd, ws, bins=bins, cmap=cm.hot)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func", tolerance=20)
def test_wrcontour():
    ax = wrcontour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func", tolerance=10)
def test_wrpdf():
    ax, params = wrpdf(ws, bins=bins)
    return ax.figure
