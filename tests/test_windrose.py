#!/usr/bin/env python

# Run all unit tests (from project root directory)
# $ pytest -vv tests

# Run a test (from project root directory)
# $ pytest -vv tests/test_windrose.py::test_windrose_np_plot_and_pd_plot

import matplotlib
import numpy as np
import pandas as pd

# import matplotlib as mpl
from matplotlib import cm as cm
from matplotlib import pyplot as plt
from numpy.testing import assert_allclose
from pandas.testing import assert_frame_equal

# from windrose import FIGSIZE_DEFAULT, DPI_DEFAULT
from windrose import (
    WindAxes,
    WindAxesFactory,
    WindroseAxes,
    clean,
    clean_df,
    plot_windrose,
    wrbar,
    wrbox,
    wrcontour,
    wrcontourf,
    wrpdf,
    wrscatter,
)

matplotlib.use("Agg")  # noqa
# Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360

df = pd.DataFrame({"speed": ws, "direction": wd})


def test_windrose_np_mpl_oo():
    bins = np.arange(0, 8, 1)

    # windrose with scatter plot
    ax = WindroseAxes.from_ax()
    ax.scatter(wd, ws, alpha=0.2)
    ax.set_legend()
    plt.savefig("tests/output/oo/scatter.png")
    plt.close()

    # windrose like a stacked histogram with normed (displayed in percent) results
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    plt.savefig("tests/output/oo/bar.png")
    plt.close()

    # Another stacked histogram representation, not normed, with bins limits
    ax = WindroseAxes.from_ax()
    ax.box(wd, ws, bins=bins)
    ax.set_legend()
    plt.savefig("tests/output/oo/box.png")
    plt.close()

    # A windrose in filled representation, with a controlled colormap
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.set_legend()
    plt.savefig("tests/output/oo/contourf.png")
    plt.close()

    # Same as above, but with contours over each filled region...
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.contour(wd, ws, bins=bins, colors="black")
    ax.set_legend()
    plt.savefig("tests/output/oo/contourf-contour.png")
    plt.close()

    # ...or without filled regions
    ax = WindroseAxes.from_ax()
    ax.contour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    ax.set_legend()
    plt.savefig("tests/output/oo/contour.png")
    plt.close()

    # print ax._info
    # plt.show()

    ax = WindAxes.from_ax()
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    plt.savefig("tests/output/oo/pdf.png")
    plt.close()


def test_windrose_np_mpl_func():
    bins = np.arange(0, 8, 1)

    wrscatter(wd, ws, alpha=0.2)
    plt.savefig("tests/output/func/scatter.png")
    plt.close()

    wrbar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    plt.savefig("tests/output/func/bar.png")
    plt.close()

    wrbox(wd, ws, bins=bins)
    plt.savefig("tests/output/func/box.png")
    plt.close()

    wrcontourf(wd, ws, bins=bins, cmap=cm.hot)
    plt.savefig("tests/output/func/contourf.png")
    plt.close()

    # ax = wrcontourf(wd, ws, bins=bin, cmap=cm.hot)
    # wrcontour(wd, ws, bins=np.arange(0, 8, 1), colors='black')
    # plt.savefig('tests/output/func/wrcontourf-contour.png')
    # plt.close()

    wrcontour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    plt.savefig("tests/output/func/contour.png")
    plt.close()

    wrpdf(ws, bins=bins)
    plt.savefig("tests/output/func/pdf.png")
    plt.close()


def test_windrose_pandas():
    bins = np.arange(0.01, 8, 1)

    kind = "scatter"
    plot_windrose(df, kind=kind, alpha=0.2)
    plt.savefig("tests/output/df/%s.png" % kind)
    plt.close()

    kind = "bar"
    plot_windrose(df, kind=kind, normed=True, opening=0.8, edgecolor="white")
    plt.savefig("tests/output/df/%s.png" % kind)
    plt.close()

    kind = "box"
    plot_windrose(df, kind=kind, bins=bins)
    plt.savefig("tests/output/df/%s.png" % kind)
    plt.close()

    kind = "contourf"
    plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot)
    plt.savefig("tests/output/df/%s.png" % kind)
    plt.close()

    kind = "contour"
    plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot, lw=3)
    plt.savefig("tests/output/df/%s.png" % kind)
    plt.close()

    kind = "pdf"
    plot_windrose(df, kind=kind, bins=bins)
    plt.savefig("tests/output/df/%s.png" % kind)
    plt.close()


def test_windaxesfactory():
    ax = WindAxesFactory.create("WindroseAxes")
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    plt.savefig("tests/output/oo/bar_from_factory.png")
    plt.close()

    ax = WindAxesFactory.create("WindAxes")
    bins = np.arange(0, 8, 1)
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    plt.savefig("tests/output/oo/pdf_from_factory.png")
    plt.close()


def test_windrose_np_plot_and_pd_plot():
    # bins = np.arange(0.01, 8, 1)
    kind = "scatter"

    plot_windrose(df, kind=kind, alpha=0.2)
    plt.savefig("tests/output/df/%s.png" % kind)
    plt.close()

    plot_windrose(wd, ws, kind=kind, alpha=0.2)
    plt.savefig("tests/output/func/%s.png" % kind)
    plt.close()


def test_windrose_pd_not_default_names():
    # bins = np.arange(0.01, 8, 1)
    kind = "scatter"
    df_not_default_names = pd.DataFrame({"wind_speed": ws, "wind_direction": wd})
    plot_windrose(
        df_not_default_names,
        kind=kind,
        alpha=0.2,
        var_name="wind_speed",
        direction_name="wind_direction",
    )


# def test_plot_by():
#     #df = pd.read_csv("samples/sample_wind_poitiers.csv", parse_dates=['Timestamp'])
#     #df['Timestamp'] = pd.to_timestamp()
#     #df = df.set_index('Timestamp')
#     #by = 'year_month'
#     #df[by] = df.index.map(lambda dt: (dt.year, dt.month))
#     #df = df.reset_index()
#     #df = df.set_index([by, 'Timestamp'])
#     #print(df)


def test_windrose_clean():
    direction = np.array([1.0, 1.0, 1.0, np.nan, np.nan, np.nan])
    var = np.array([2.0, 0.0, np.nan, 2.0, 0.0, np.nan])
    actual_direction, actual_var = clean(direction, var)
    expected_direction = np.array([1.0])
    expected_var = np.array([2.0])
    assert_allclose(actual_direction, expected_direction)
    assert_allclose(actual_var, expected_var)


def test_windrose_clean_df():
    df = pd.DataFrame(
        {
            "direction": [1.0, 1.0, 1.0, np.nan, np.nan, np.nan],
            "speed": [2.0, 0.0, np.nan, 2.0, 0.0, np.nan],
        }
    )
    actual_df = clean_df(df)
    expected_df = pd.DataFrame(
        {
            "direction": [1.0],
            "speed": [2.0],
        }
    )
    assert_frame_equal(actual_df, expected_df)
