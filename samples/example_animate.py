#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
This sample need to be improve to provide
a clean API to output animation
"""

import click

from math import pi

import sys
import traceback

import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.cm as cm

import pandas as pd
pd.set_option('max_rows', 10)
import numpy as np

from windrose import (WindroseAxes, WindAxes, plot_windrose, 
                        FIGSIZE_DEFAULT, DPI_DEFAULT)

S_FIGSIZE_DEFAULT = ",".join(map(str, FIGSIZE_DEFAULT))

def get_by_func(by=None, by_func=None):
    if by is None and by_func is None:
        by = 'MS'

    if by in ['year', 'yearly', 'Y']:
        return lambda dt: (dt.year, dt.month, dt.day)
    elif by in ['month', 'monthly', 'MS']:  # MS: month start
        return lambda dt: (dt.year, dt.month)
    elif by in ['day', 'daily', 'D']:
        return lambda dt: (dt.year, dt.month, dt.day)
    elif by is None and func is not None:
        return by_func
    else:
        raise NotImplementedError("'%s' is not an allowed 'by' parameter" % by)

def generate(df_all, func, copy=True):
    if copy:
        df_all = df_all.copy()
    df_all['by'] = df_all.index.map(func)
    df = df_all.reset_index().set_index(['by', df_all.index.name])
    for by_val in df.index.levels[0]:
        yield df.loc[by_val]

def count(df_all, func):
    return len(np.unique(df_all.index.map(func)))

@click.command()
@click.option("--filename", default="samples/sample_wind_poitiers.csv", help="Input filename")
@click.option("--exit_at", default=0, help="premature exit (int) - must be > 1")
@click.option("--by", default='month', help="Animate by (year, month, day...)")
@click.option("--filename_out", default="windrose_animation.mp4", help="Output filename")
@click.option("--dpi", default=DPI_DEFAULT, help="Dot per inch for plot generation")
@click.option("--figsize", default=S_FIGSIZE_DEFAULT, help="Figure size x,y - default=%s" % S_FIGSIZE_DEFAULT)
@click.option("--fps", default=7, help="Number of frame per seconds for video generation")
@click.option("--bins_min", default=0.01, help="Bins minimum value")
@click.option("--bins_max", default=20, help="Bins maximum value")
@click.option("--bins_step", default=2, help="Bins step value")
@click.option("--fontname", default="Courier New", help="Font name")
def main(filename, exit_at, by, dpi, figsize, fps, bins_min, bins_max, bins_step, fontname, filename_out):
    # convert figsize (string like "8,9" to a list of float [8.0, 9.0]
    figsize = figsize.split(",")
    figsize = map(float, figsize)

    by_func = get_by_func(by)

    # Read CSV file to a Pandas DataFrame
    df_all = pd.read_csv(filename)
    df_all['Timestamp'] = pd.to_datetime(df_all['Timestamp'])
    df_all = df_all.set_index('Timestamp')

    df_all.index = df_all.index.tz_localize('UTC').tz_convert('UTC')

    dt_start = df_all.index[0]
    dt_end = df_all.index[-1]
    print("First dt: %s" % dt_start)
    print("Last  dt: %s" % dt_end)
    td = dt_end - dt_start
    print("      td: %s" % td)
    Nslides = count(df_all, by_func)
    print("  Slides: %d" % Nslides)

    # Define bins
    bins = np.arange(bins_min, bins_max, bins_step)

    # Create figure
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='w', edgecolor='w')

    # Create a video writer (ffmpeg can create MPEG files)
    FFMpegWriter = matplotlib.animation.writers['ffmpeg']
    metadata = dict(title='windrose', artist='windrose',
            comment="""Made with windrose
http://www.github.com/scls19fr/windrose""")
    writer = FFMpegWriter(fps=fps, metadata=metadata)

    print("")

    with writer.saving(fig, filename_out, 100):
        try:
            for i, df in enumerate(generate(df_all, by_func)):
                dt1 = df.index[0]
                dt2 = df.index[-1]
                td = dt2 - dt1
                msg = """  Slide %s/%s
    From %s
    to %s
    td %s
""" % (i+1, Nslides, dt1, dt2, td)
                print(msg)
                title = "  From %s\n    to %s" % (dt1, dt2)
    
                try:
                    ax = WindroseAxes.from_ax(fig=fig) # scatter, bar, box, contour, contourf
                    
                    direction = df['direction'].values
                    var = df['speed'].values
                    
                    #ax.scatter(direction, var, alpha=0.2)
                    #ax.set_xlim([-bins[-1], bins[-1]])
                    #ax.set_ylim([-bins[-1], bins[-1]])

                    #ax.bar(direction, var, bins=bins, normed=True, opening=0.8, edgecolor='white')

                    #ax.box(direction, var, bins=bins)

                    #ax.contour(direction, var, cmap=cm.hot, lw=3, bins=bins)

                    ax.contourf(direction, var, bins=bins, cmap=cm.hot)
                    ax.contour(direction, var, bins=bins, colors='black', lw=3)

                    ax.set_legend()

                    #ax = WindAxes.from_ax(fig=fig) # pdf: probability density function
                    #ax.pdf(var, bins=bins)
                    #ax.set_xlim([0, bins[-1]])
                    #ax.set_ylim([0, 0.4])

                    ax.set_title(title, fontname=fontname)

                    writer.grab_frame()
                except KeyboardInterrupt:
                    return
                except Exception as e:
                    print(traceback.format_exc(), file=sys.stderr)

                print("")

                fig.clf()
                if i > exit_at - 1 and exit_at != 0: # exit_at must be > 1
                    break
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)

        N = i + 1
        print("Number of slides: %d" % N)


    #plt.show()

    print("")
    print("Save file to '%s'" % filename_out)

if __name__ == "__main__":
    main()
