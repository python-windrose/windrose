#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
sample using "by" keyword
"""

import click

import matplotlib
#matplotlib.use("Agg")

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation

import matplotlib.cm as cm
import numpy as np
from math import pi

from windrose import WindroseAxes, WindAxes, plot_windrose, clean, FIGSIZE_DEFAULT, DPI_DEFAULT

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

    # Read CSV file to a Pandas DataFrame
    df = pd.read_csv(filename)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.set_index('Timestamp')
    #df = df.iloc[-10000:,:]
    df.index = df.index.tz_localize('UTC').tz_convert('UTC')

    # Get Numpy arrays from DataFrame
    direction = df['direction'].values
    var = df['speed'].values
    index = df.index.to_datetime() #Fixed: .values -> to_datetime()
    by = df.index.map(by_func_monthly)
    by_unique = np.unique(by)
    #print(by_unique)

    for by_value in by_unique:
        #by_value = (2011, 5)

        #mask = (by == by_value).all(axis=1)
        # ToFix: see http://stackoverflow.com/questions/32005403/boolean-indexing-with-numpy-array-and-tuples

        mask = (pd.Series(by) == by_value).values

        #print(mask)

        index_masked = index[mask]
        var_masked = var[mask]
        direction_masked = direction[mask]

        # Define bins
        bins = np.arange(bins_min, bins_max, bins_step)

        # Create figure
        #fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='w', edgecolor='w')

        #Same as above, but with contours over each filled region...
        ax = WindroseAxes.from_ax()
        ax.contourf(direction_masked, var_masked, bins=bins, cmap=cm.hot)
        ax.contour(direction_masked, var_masked, bins=bins, colors='black')
        fontname = "Courier"
        #title = by_value
        dt1 = index_masked[0]
        dt2 = index_masked[-1]
        #dt1 = df.index[mask][0]
        #dt2 = df.index[mask][-1]
        td = dt2 - dt1
        title = "From %s\n  to %s" % (dt1, dt2)

        ax.set_title(title, fontname=fontname)
        ax.set_legend()

        plt.show()

    #time.sleep(10)

    #print("Save file to '%s'" % filename_out)

if __name__ == "__main__":
    main()
