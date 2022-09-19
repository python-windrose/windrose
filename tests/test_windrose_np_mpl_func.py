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


@pytest.mark.mpl_image_compare(baseline_dir="output/func")
def test_wrscatter():
    ax = wrscatter(wd, ws, alpha=0.2)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func")
def test_wrbar():
    ax = wrbar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func")
def test_wrbox():
    ax = wrbox(wd, ws, bins=bins)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func")
def test_wrcontourf():
    ax = wrcontourf(wd, ws, bins=bins, cmap=cm.hot)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func")
def test_wrcontour():
    ax = wrcontour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/func")
def test_wrpdf():
    ax, params = wrpdf(ws, bins=bins)
    return ax.figure
