#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from windrose import plot_windrose
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np


def main():
    df = pd.read_csv("samples/sample_wind_poitiers.csv", parse_dates=["Timestamp"])
    # df['Timestamp'] = pd.to_timestamp()
    df = df.set_index("Timestamp")

    # N = 500
    # ws = np.random.random(N) * 6
    # wd = np.random.random(N) * 360
    # df = pd.DataFrame({'speed': ws, 'direction': wd})

    print(df)
    print(df.dtypes)

    bins = np.arange(0.01, 8, 1)
    # bins = np.arange(0, 8, 1)[1:]
    plot_windrose(df, kind="contour", bins=bins, cmap=cm.hot, lw=3, rmax=20000)
    plt.show()

    bins = np.arange(0, 30 + 1, 1)
    bins = bins[1:]

    ax, params = plot_windrose(df, kind="pdf", bins=bins)
    print("Weibull params:")
    print(params)
    # plt.savefig("screenshots/pdf.png")
    plt.show()


if __name__ == "__main__":
    main()
