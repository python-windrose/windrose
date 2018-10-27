#!/usr/bin/env python
# -*- coding: utf-8 -*-

from windrose import WindroseAxes
from windrose import WindAxes

from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np


def main():
    # Create wind speed and direction variables
    N = 500
    ws = np.random.random(N) * 6
    wd = np.random.random(N) * 360

    ax = WindroseAxes.from_ax()
    ax.scatter(wd, ws, alpha=0.2)
    ax.set_legend()

    # windrose like a stacked histogram with normed (displayed in percent) results
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()

    # Another stacked histogram representation, not normed, with bins limits
    ax = WindroseAxes.from_ax()
    bins = np.arange(0, 8, 1)
    ax.box(wd, ws, bins=bins)
    ax.set_legend()

    # A windrose in filled representation, with a controled colormap
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.set_legend()

    # Same as above, but with contours over each filled region...
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.contour(wd, ws, bins=bins, colors="black")
    ax.set_legend()

    # ...or without filled regions
    ax = WindroseAxes.from_ax()
    ax.contour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    ax.set_legend()

    # print ax._info
    # plt.show()

    ax = WindAxes.from_ax()
    bins = np.arange(0, 6 + 1, 0.5)
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    plt.show()


if __name__ == "__main__":
    main()
