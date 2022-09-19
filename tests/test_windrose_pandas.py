# generate the baseline: pytest tests/test_windrose_pandas.py --mpl-generate-path=tests/output/df/


import matplotlib
import numpy as np
import pandas as pd
import pytest
from matplotlib import cm as cm

from windrose import plot_windrose

matplotlib.use("Agg")  # noqa
np.random.seed(0)
# Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360
bins = np.arange(0.01, 8, 1)

df = pd.DataFrame({"speed": ws, "direction": wd})


@pytest.mark.mpl_image_compare(baseline_dir="output/df")
def test_scatter():
    kind = "scatter"
    ax = plot_windrose(df, kind=kind, alpha=0.2)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/df")
def test_bar():
    kind = "bar"
    ax = plot_windrose(df, kind=kind, normed=True, opening=0.8, edgecolor="white")
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/df")
def test_box():
    kind = "box"
    ax = plot_windrose(df, kind=kind, bins=bins)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/df")
def test_contourf():
    kind = "contourf"
    ax = plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/df")
def test_contour():
    kind = "contour"
    ax = plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot, lw=3)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/df")
def test_pdf():
    kind = "pdf"
    ax, params = plot_windrose(df, kind=kind, bins=bins)
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/df")
def test_windrose_np_plot_and_pd_plot():
    # Not really pandas but this is an orphan test and fits the plot_windrose tests.
    kind = "scatter"
    ax = plot_windrose(wd, ws, kind=kind, alpha=0.2)
    return ax.figure
