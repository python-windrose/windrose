# generate the baseline: pytest tests/test_windrose_np_mpl_oo.py --mpl-generate-path=tests/output/oo/

import matplotlib
import numpy as np
import pandas as pd
import pytest
from matplotlib import cm as cm

from windrose import WindAxes, WindroseAxes

matplotlib.use("Agg")  # noqa
np.random.seed(0)
# Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360
bins = np.arange(0, 8, 1)

df = pd.DataFrame({"speed": ws, "direction": wd})


@pytest.mark.mpl_image_compare(baseline_dir="output/oo")
def test_windrose_with_scatter_plot():
    ax = WindroseAxes.from_ax()
    ax.scatter(wd, ws, alpha=0.2)
    ax.set_legend()
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/oo", tolerance=15.5)
def test_windrose_stacked_histogram_normed():
    # windrose like a stacked histogram with normed (displayed in percent) results
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/oo", tolerance=6.5)
def test_windrose_stacked_histogram_not_normed_binned():
    # Another stacked histogram representation, not normed, with bins limits
    ax = WindroseAxes.from_ax()
    ax.box(wd, ws, bins=bins)
    ax.set_legend()
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/oo")
def test_filled_with_colormap():
    # A windrose in filled representation, with a controlled colormap
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.set_legend()
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/oo")
def test_filled_with_colormap_contours():
    # Same as above, but with contours over each filled region...
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.contour(wd, ws, bins=bins, colors="black")
    ax.set_legend()
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/oo")
def test_without_filled_with_colormap_contours():
    ax = WindroseAxes.from_ax()
    ax.contour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    ax.set_legend()
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/oo")
def test_pdf():
    ax = WindAxes.from_ax()
    bins = np.arange(0, 8, 1)
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    return ax.figure
