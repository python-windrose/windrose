#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
sample using "by" keyword
"""

import numpy as np
import matplotlib.pyplot as plt

import click

import matplotlib
#matplotlib.use("Agg")

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.backends.backend_pdf import PdfPages

import matplotlib.cm as cm
import numpy as np
from math import pi
from numpy import sin, cos

from windrose import WindroseAxes, WindAxes, plot_windrose, clean, FIGSIZE_DEFAULT, DPI_DEFAULT
from windrose import wrscatter

import sys
import traceback

import time

S_FIGSIZE_DEFAULT = ",".join(map(str, FIGSIZE_DEFAULT))

def by_func_yearly(dt):
    return dt.year

def by_func_monthly(dt):
    return dt.year, dt.month

def by_func_daily(dt):
    return dt.year, dt.month, dt.day

@click.command()
@click.option("--filename", default="samples/sample_wind_poitiers.csv", help="Input filename")
@click.option("--filename_out", default="windrose_animation.mp4", help="Output filename")
@click.option("--dpi", default=DPI_DEFAULT, help="Dot per inch for plot generation")
@click.option("--figsize", default=S_FIGSIZE_DEFAULT, help="Figure size x,y - default=%s" % S_FIGSIZE_DEFAULT)
@click.option("--fps", default=7, help="Number of frame per seconds for video generation")
@click.option("--bins_min", default=0.01, help="Bins minimum value")
@click.option("--bins_max", default=20, help="Bins maximum value")
@click.option("--bins_step", default=2, help="Bins step value")
def main(filename, dpi, figsize, fps, bins_min, bins_max, bins_step, filename_out):
    # convert figsize (string like "8,9" to a list of float [8.0, 9.0]
    figsize = figsize.split(",")
    figsize = map(float, figsize)
    width, height = figsize

    # Read CSV file to a Pandas DataFrame
    df_all = pd.read_csv(filename)
    df_all['Timestamp'] = pd.to_datetime(df_all['Timestamp'])
    df_all = df_all.set_index('Timestamp')
    df_all.index = df_all.index.tz_localize('UTC').tz_convert('UTC')
    #df_all = df_all.iloc[-10000:,:]    
    df_all = df_all['2011-07-01':'2012-12-31']

    # Get Numpy arrays from DataFrame
    direction_all = df_all['direction'].values
    var_all = df_all['speed'].values
    index_all = df_all.index.to_datetime() #Fixed: .values -> to_datetime()
    by_all = df_all.index.map(by_func_monthly)
    by_unique = np.unique(by_all)
    print(by_unique)

    # Define bins
    bins = np.arange(bins_min, bins_max, bins_step)

    (ncols, nrows) = (4, 3)
    offset = 6

    for i, by_value in enumerate(by_unique):
        if (i + offset) % (ncols*nrows) == 0 or i==0:
            fig, axs = plt.subplots(nrows=nrows, ncols=ncols, dpi=dpi, facecolor='w', edgecolor='w')
            #print(fig, axs)

        i_sheet, sheet_pos = divmod(i + offset, ncols*nrows)
        i_row, i_col  = divmod(sheet_pos, ncols)

        ax = axs[i_row][i_col]

        mask = (pd.Series(by_all) == by_value).values

        index = index_all[mask]
        var = var_all[mask]
        direction = direction_all[mask]

        #df = pd.DataFrame([var, direction], index=['Speed', 'Direction'], columns=index).transpose()
        #df.index.name = 'DateTime'
        #print(df)

        # Create figure
        #fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='w', edgecolor='w')

        ax.scatter(var*sin(pi / 180 * direction), var*cos(pi / 180 * direction), alpha=0.1)
        v = 40
        ax.set_xlim(-v, v)
        ax.set_ylim(-v, v)
        #wrscatter(direction, var, ax=ax)

        #Same as above, but with contours over each filled region...
        #ax = WindroseAxes.from_ax(ax)
        #ax.contourf(direction, var, bins=bins, cmap=cm.hot)
        #ax.contour(direction, var, bins=bins, colors='black')

        dt1 = index[0]
        dt2 = index[-1]
        #dt1 = df.index[mask][0]
        #dt2 = df.index[mask][-1]
        td = dt2 - dt1

        #title = by_value
        #title = "From %s\n  to %s" % (dt1, dt2)
        title = "%04d-%02d" % (by_value[0], by_value[1])
        fontname = "Courier"
        ax.set_title(title, fontname=fontname)

        #ax.set_legend()

        if (i + offset + 1) % (ncols*nrows) == 0:
            plt.show()

    #time.sleep(10)

    #print("Save file to '%s'" % filename_out)

if __name__ == "__main__":
    main()
