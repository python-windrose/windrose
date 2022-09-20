# generate the baseline: pytest tests/test_windrose_factory.py --mpl-generate-path=tests/output


import matplotlib
import numpy as np
import pandas as pd
import pytest

from windrose import WindAxesFactory

matplotlib.use("Agg")  # noqa
np.random.seed(0)
# Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360
bins = np.arange(0.01, 8, 1)

df = pd.DataFrame({"speed": ws, "direction": wd})


@pytest.mark.mpl_image_compare(baseline_dir="output/")
def test_bar_from_factory():
    ax = WindAxesFactory.create("WindroseAxes")
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    return ax.figure


@pytest.mark.mpl_image_compare(baseline_dir="output/")
def test_pdf_from_factory():
    ax = WindAxesFactory.create("WindAxes")
    bins = np.arange(0, 8, 1)
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    return ax.figure
