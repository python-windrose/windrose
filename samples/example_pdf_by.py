#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
Example to create a PDF
Monthly windrose axe
One figure per year
"""


import click

import datetime

# import time

from math import pi

# import matplotlib
import matplotlib.pyplot as plt

# import matplotlib.animation
from matplotlib.backends.backend_pdf import PdfPages

# import matplotlib.cm as cm

import numpy as np
from numpy import sin, cos
import pandas as pd

from windrose import WindroseAxes, WindAxes, plot_windrose, clean  # noqa
from windrose import wrscatter, wrcontour, wrcontourf  # noqa

FIGSIZE_DEFAULT = (16, 12)
S_FIGSIZE_DEFAULT = ",".join(map(str, FIGSIZE_DEFAULT))

DPI_DEFAULT = 40


def by_func_yearly(dt):
    return dt.year


def by_func_monthly(dt):
    return dt.year, dt.month


def by_func_daily(dt):
    return dt.year, dt.month, dt.day


@click.command()
@click.option(
    "--filename", default="samples/sample_wind_poitiers.csv", help="Input filename"
)
@click.option("--filename_out", default="windrose.pdf", help="Output filename")
@click.option("--dpi", default=DPI_DEFAULT, help="Dot per inch for plot generation")
@click.option(
    "--figsize",
    default=S_FIGSIZE_DEFAULT,
    help="Figure size x,y - default=%s" % S_FIGSIZE_DEFAULT,
)
@click.option("--bins_min", default=0.01, help="Bins minimum value")
@click.option("--bins_max", default=20, help="Bins maximum value")
@click.option("--bins_step", default=2, help="Bins step value")
@click.option("--fontname", default="Courier New", help="Font name")
@click.option("--show/--no-show", default=False, help="Show figure")
@click.option("--dt_from", default="", help="Datetime from")
@click.option("--dt_to", default="", help="Datetime to")
@click.option("--offset", default=0, help="Axe figure offset")
@click.option("--ncols", default=4, help="Number of columns per figure")
@click.option("--nrows", default=3, help="Number of rows per figure")
def main(
    filename,
    dt_from,
    dt_to,
    dpi,
    figsize,
    bins_min,
    bins_max,
    bins_step,
    ncols,
    nrows,
    fontname,
    show,
    filename_out,
    offset,
):

    # convert figsize (string like "8,9" to a list of float [8.0, 9.0]
    figsize = figsize.split(",")
    figsize = tuple(map(float, figsize))
    width, height = figsize

    # Read CSV file to a Pandas DataFrame
    df_all = pd.read_csv(filename)
    df_all["Timestamp"] = pd.to_datetime(df_all["Timestamp"])
    df_all = df_all.set_index("Timestamp")
    df_all.index = df_all.index.tz_localize("UTC").tz_convert("UTC")
    # df_all = df_all.iloc[-10000:,:]
    # df_all = df_all['2011-07-01':'2012-12-31']
    if dt_from == "":
        dt_from = df_all.index[0]
    if dt_to == "":
        dt_to = df_all.index[-1]
    df_all = df_all[dt_from:dt_to]

    # Get Numpy arrays from DataFrame
    direction_all = df_all["direction"].values
    var_all = df_all["speed"].values
    # index_all = df_all.index.to_datetime()  # Fixed: .values -> to_datetime()
    by_all = df_all.index.map(by_func_monthly)
    by_unique = np.unique(by_all)
    print(by_unique)

    # Define bins
    # bins = np.arange(bins_min, bins_max, bins_step)

    with PdfPages(filename_out) as pdf:

        for i, by_value in enumerate(by_unique):
            print("processing: %s" % str(by_value))

            if (i + offset) % (ncols * nrows) == 0 or i == 0:
                # Create figure and axes
                fig, axs = plt.subplots(
                    nrows=nrows,
                    ncols=ncols,
                    figsize=figsize,
                    dpi=dpi,
                    facecolor="w",
                    edgecolor="w",
                )
                print("%r\n%r\n%r" % (fig, fig.axes, axs))

            i_sheet, sheet_pos = divmod(i + offset, ncols * nrows)
            i_row, i_col = divmod(sheet_pos, ncols)

            # ax = axs[i_row][i_col]
            ax = fig.axes[sheet_pos]

            mask = (pd.Series(by_all) == by_value).values

            # index = index_all[mask]
            var = var_all[mask]
            direction = direction_all[mask]

            # df = pd.DataFrame([var, direction], index=['Speed', 'Direction'], columns=index).transpose()
            # df.index.name = 'DateTime'
            # print(df)

            Vx = var * sin(pi / 180 * direction)
            Vy = var * cos(pi / 180 * direction)
            ax.scatter(Vx, Vy, alpha=0.1)
            v = 40
            ax.set_xlim(-v, v)
            ax.set_ylim(-v, v)

            # rect = [0.1, 0.1, 0.8, 0.8]
            # ax = WindroseAxes(fig, rect, facecolor='w')
            # wrscatter(direction, var, ax=ax) # ToFix!!!! TypeError: Input must be a 2D array.

            # print(direction)
            # print(var)
            # print(ax)
            # wrcontour(direction, var, ax=ax) # ToFix!!!! TypeError: Input must be a 2D array.

            # Same as above, but with contours over each filled region...
            # ToFix!!!! TypeError: Input must be a 2D array.
            # ax = WindroseAxes.from_ax(ax)
            # rect = [0.1, 0.1, 0.8, 0.8]
            # #axs[i_row][i_col] = WindroseAxes(fig, rect, facecolor='w')
            # #axs[i_row][i_col] = WindroseAxes.from_ax(fig=fig)
            # ax = WindroseAxes(fig, rect, facecolor='w')
            # fig.axes[i + offset] = ax
            # ax.contourf(direction, var, bins=bins, cmap=cm.hot)
            # ax.contour(direction, var, bins=bins, colors='black')

            # dt1 = index[0]
            # dt2 = index[-1]
            # dt1 = df.index[mask][0]
            # dt2 = df.index[mask][-1]
            # td = dt2 - dt1

            # title = by_value
            # title = "From %s\n  to %s" % (dt1, dt2)
            # title = "%04d-%02d" % (by_value[0], by_value[1])
            dt = datetime.date(by_value[0], by_value[1], 1)
            fmt = "%B"  # "%Y %B"  # Month
            title = dt.strftime(fmt)
            ax.set_title(title, fontname=fontname)

            # ax.set_legend()

            fig_title = dt.strftime("%Y")  # Year
            fig.suptitle(fig_title)

            remaining = (i + offset + 1) % (ncols * nrows)
            if remaining == 0:
                save_figure(fig, pdf, show, fig_title)

        if remaining != 0:
            save_figure(fig, pdf, show, fig_title)

        # time.sleep(10)

        print("Save file to '%s'" % filename_out)

        print("remaining: %d" % remaining)


def save_figure(fig, pdf, show, fig_title):
    filename = "windrose_%s.png" % fig_title
    print("save_figure: %s" % filename)
    if show:
        plt.show()
    fig.savefig(filename)  # Save to image
    pdf.savefig(fig)


if __name__ == "__main__":
    main()
