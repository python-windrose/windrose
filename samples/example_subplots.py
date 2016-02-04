#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm

from windrose import WindroseAxes

pd.set_option('max_rows', 10)


def get_by_func(by=None, by_func=None):
    if by is None and by_func is None:
        by = 'MS'

    if by in ['year', 'yearly', 'Y']:
        return lambda dt: dt.year
    elif by in ['month', 'monthly', 'MS']:  # MS: month start
        return lambda dt: (dt.year, dt.month)
    elif by in ['day', 'daily', 'D']:
        return lambda dt: (dt.year, dt.month, dt.day)
    elif by is None and by_func is not None:
        return by_func
    else:
        raise NotImplementedError("'%s' is not an allowed 'by' parameter" % by)


def tuple_position(i, nrows, ncols):
    i_sheet, sheet_pos = divmod(i, ncols * nrows)
    i_row, i_col = divmod(sheet_pos, ncols)
    return i_sheet, i_row, i_col


def main():
    df_all = pd.read_csv("samples/sample_wind_poitiers.csv", parse_dates=['Timestamp'])
    df_all = df_all.set_index('Timestamp')

    f_year = get_by_func('year')
    df_all['by_page'] = df_all.index.map(f_year)
    f_month = get_by_func('month')
    df_all['by'] = df_all.index.map(f_month)

    df_all = df_all.reset_index().set_index(['by_page', 'by', 'Timestamp'])

    print(df_all)

    year = 2014

    nrows, ncols = 3, 4
    margin_pct = 0.1
    margin_pct_x, margin_pct_y = margin_pct, margin_pct
    width, height = (1.0 - margin_pct_x) / ncols, (1.0 - margin_pct_y) / nrows

    for month in range(1, 13):
        df = df_all.loc[year].loc[(year, month)]
        i_sheet, i_row, i_col = tuple_position(month - 1, nrows, ncols)
        assert i_sheet == 0
        bins = np.arange(0.01, 8, 1)
        direction = df['direction'].values
        var = df['speed'].values

        fig = plt.gcf()
        rect = [i_col * width + margin_pct_x / 2, 1 - (i_row + 1) * height - margin_pct_y / 2, width, height]  # [left, bottom, width, height]
        ax = WindroseAxes(fig, rect, rmax=1000)
        # ax.set_title(month)
        fig.add_axes(ax)
        # ax.contour(direction, var, bins=bins, colors='black', lw=3)
        ax.contourf(direction, var, bins=bins, cmap=cm.hot)
        ax.contour(direction, var, bins=bins, colors='black')

    plt.show()

if __name__ == "__main__":
    main()
