#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

import datetime
import pandas as pd

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm

import windrose  # noqa

pd.set_option("max_rows", 10)


def get_by_func(by=None, by_func=None):
    if by is None and by_func is None:
        by = "MS"

    if by in ["year", "yearly", "Y"]:
        return lambda dt: dt.year
    elif by in ["month", "monthly", "MS"]:  # MS: month start
        return lambda dt: (dt.year, dt.month)
    elif by in ["day", "daily", "D"]:
        return lambda dt: (dt.year, dt.month, dt.day)
    elif by is None and by_func is not None:
        return by_func
    else:
        raise NotImplementedError("'%s' is not an allowed 'by' parameter" % by)


def tuple_position(i, nrows, ncols):
    i_sheet, sheet_pos = divmod(i, ncols * nrows)
    i_row, i_col = divmod(sheet_pos, ncols)
    return i_sheet, i_row, i_col


@click.command()
@click.option(
    "--filename", default="samples/sample_wind_poitiers.csv", help="Input filename"
)
@click.option("--year", default=2014, help="Year")
def main(filename, year):
    df_all = pd.read_csv(filename, parse_dates=["Timestamp"])
    df_all = df_all.set_index("Timestamp")

    f_year = get_by_func("year")
    df_all["by_page"] = df_all.index.map(f_year)
    f_month = get_by_func("month")
    df_all["by"] = df_all.index.map(f_month)

    df_all = df_all.reset_index().set_index(["by_page", "by", "Timestamp"])

    print(df_all)

    nrows, ncols = 3, 4
    fig = plt.figure()
    bins = np.arange(0.01, 8, 1)

    fig.suptitle("Wind speed - %d" % year)
    for month in range(1, 13):
        ax = fig.add_subplot(nrows, ncols, month, projection="windrose")
        title = datetime.datetime(year, month, 1).strftime("%b")
        ax.set_title(title)
        try:
            df = df_all.loc[year].loc[(year, month)]
        except KeyError:
            continue
        direction = df["direction"].values
        var = df["speed"].values
        # ax.contour(direction, var, bins=bins, colors='black', lw=3)
        ax.contourf(direction, var, bins=bins, cmap=cm.hot)
        ax.contour(direction, var, bins=bins, colors="black")

    plt.show()


if __name__ == "__main__":
    main()
