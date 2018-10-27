#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run all unit tests (from project root directory)
# $ pytest -vv tests

# Run a test (from project root directory)
# $ pytest -vv tests/test_windrose.py::test_windrose_np_plot_and_pd_plot

import matplotlib

matplotlib.use("Agg")  # noqa

# import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import cm as cm

from windrose import WindroseAxes
from windrose import WindAxes
from windrose import WindAxesFactory

# from windrose import FIGSIZE_DEFAULT, DPI_DEFAULT
from windrose import wrbar, wrbox, wrcontour, wrcontourf, wrpdf, wrscatter
from windrose import plot_windrose

import numpy as np
import pandas as pd


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

    # windrose like a stacked histogram with normed (displayed in percent) results
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    plt.savefig("tests/output/oo/bar.png")

    # Another stacked histogram representation, not normed, with bins limits
    ax = WindroseAxes.from_ax()
    ax.box(wd, ws, bins=bins)
    ax.set_legend()
    plt.savefig("tests/output/oo/box.png")

    # A windrose in filled representation, with a controled colormap
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.set_legend()
    plt.savefig("tests/output/oo/contourf.png")

    # Same as above, but with contours over each filled region...
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.contour(wd, ws, bins=bins, colors="black")
    ax.set_legend()
    plt.savefig("tests/output/oo/contourf-contour.png")

    # ...or without filled regions
    ax = WindroseAxes.from_ax()
    ax.contour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    ax.set_legend()
    plt.savefig("tests/output/oo/contour.png")

    # print ax._info
    # plt.show()

    ax = WindAxes.from_ax()
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    plt.savefig("tests/output/oo/pdf.png")


def test_windrose_np_mpl_func():
    bins = np.arange(0, 8, 1)

    wrscatter(wd, ws, alpha=0.2)
    plt.savefig("tests/output/func/scatter.png")

    wrbar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    plt.savefig("tests/output/func/bar.png")

    wrbox(wd, ws, bins=bins)
    plt.savefig("tests/output/func/box.png")

    wrcontourf(wd, ws, bins=bins, cmap=cm.hot)
    plt.savefig("tests/output/func/contourf.png")

    # ax = wrcontourf(wd, ws, bins=bin, cmap=cm.hot)
    # wrcontour(wd, ws, bins=np.arange(0, 8, 1), colors='black')
    # plt.savefig('tests/output/func/wrcontourf-contour.png')

    wrcontour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    plt.savefig("tests/output/func/contour.png")

    wrpdf(ws, bins=bins)
    plt.savefig("tests/output/func/pdf.png")


def test_windrose_pandas():
    bins = np.arange(0.01, 8, 1)

    kind = "scatter"
    plot_windrose(df, kind=kind, alpha=0.2)
    plt.savefig("tests/output/df/%s.png" % kind)

    kind = "bar"
    plot_windrose(df, kind=kind, normed=True, opening=0.8, edgecolor="white")
    plt.savefig("tests/output/df/%s.png" % kind)

    kind = "box"
    plot_windrose(df, kind=kind, bins=bins)
    plt.savefig("tests/output/df/%s.png" % kind)

    kind = "contourf"
    plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot)
    plt.savefig("tests/output/df/%s.png" % kind)

    kind = "contour"
    plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot, lw=3)
    plt.savefig("tests/output/df/%s.png" % kind)

    kind = "pdf"
    plot_windrose(df, kind=kind, bins=bins)
    plt.savefig("tests/output/df/%s.png" % kind)


def test_windaxesfactory():
    ax = WindAxesFactory.create("WindroseAxes")
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    plt.savefig("tests/output/oo/bar_from_factory.png")

    ax = WindAxesFactory.create("WindAxes")
    bins = np.arange(0, 8, 1)
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    plt.savefig("tests/output/oo/pdf_from_factory.png")


def test_windrose_np_plot_and_pd_plot():
    # bins = np.arange(0.01, 8, 1)
    kind = "scatter"

    plot_windrose(df, kind=kind, alpha=0.2)
    plt.savefig("tests/output/df/%s.png" % kind)

    plot_windrose(wd, ws, kind=kind, alpha=0.2)
    plt.savefig("tests/output/func/%s.png" % kind)


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
