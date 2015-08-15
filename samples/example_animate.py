#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
This sample need to be improve to provide
a clean API to output animation
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

S_FIGSIZE_DEFAULT = ",".join(map(str, FIGSIZE_DEFAULT))

@click.command()
@click.option("--filename", default="samples/sample_wind_poitiers.csv", help="Input filename")
@click.option("--exit_at", default=0, help="premature exit (int) - must be > 1")
@click.option("--size", default=36 * 4, help="size of window")
@click.option("--offset", default=3 + 6 * 6 + 24 * 6 * 365 * 2 - 24 * 6 * 65, help="data offset")
@click.option("--filename_out", default="windrose_animation.mp4", help="Output filename")
@click.option("--dpi", default=DPI_DEFAULT, help="Dot per inch for plot generation")
@click.option("--figsize", default=S_FIGSIZE_DEFAULT, help="Figure size x,y - default=%s" % S_FIGSIZE_DEFAULT)
@click.option("--fps", default=7, help="Number of frame per seconds for video generation")
@click.option("--bins_min", default=0.01, help="Bins minimum value")
@click.option("--bins_max", default=20, help="Bins maximum value")
@click.option("--bins_step", default=2, help="Bins step value")
@click.option("--fontname", default="Courier New", help="Font name")
def main(filename, exit_at, size, offset, dpi, figsize, fps, bins_min, bins_max, bins_step, fontname, filename_out):
    # convert figsize (string like "8,9" to a list of float [8.0, 9.0]
    figsize = figsize.split(",")
    figsize = map(float, figsize)

    # Read CSV file to a Pandas DataFrame
    df_all = pd.read_csv(filename)
    df_all['Timestamp'] = pd.to_datetime(df_all['Timestamp'])
    df_all = df_all.set_index('Timestamp')
    #df_all = df_all.iloc[-10000:,:]
    df_all.index = df_all.index.tz_localize('UTC').tz_convert('UTC')

    # Get Numpy arrays from DataFrame
    direction_all = df_all['direction'].values
    var_all = df_all['speed'].values
    index_all = df_all.index.to_datetime() #.values -> .to_datetime()

    # Define bins
    bins = np.arange(bins_min, bins_max, bins_step)

    # Create figure
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='w', edgecolor='w')

    # Create a video writer (ffmpeg can create MPEG files)
    FFMpegWriter = mpl.animation.writers['ffmpeg']
    metadata = dict(title='windrose', artist='windrose',
            comment="""Made with windrose
http://www.github.com/scls19fr/windrose""")
    writer = FFMpegWriter(fps=fps, metadata=metadata)

    dt0 = index_all[offset]
    print("size: %d" % size)
    print("offset: %d" % offset)
    print("First dt: %s" % dt0)

    print("")

    dt2 = None
    i = 0
    with writer.saving(fig, filename_out, 100):
        #for i in range(1000): # 100
        try:
            while True: # loop until fails (end of data)
                print("Processing %d" % (i + 1))
                i1 = offset + i*size
                i2 = offset + (i+1)*size + 1

                index = index_all[i1:i2]
                dt1 = index[0]
                dt2 = index[-1]
                td = dt2 - dt1
                title = "  From %s\n    to %s" % (dt1, dt2)
                print(title)
                print("    td %r" % td)
                #print("    td %r" % td.astype('timedelta64[m]'))
    
                try:
                    direction = direction_all[i1:i2]
                    var = var_all[i1:i2]

                    ax = WindroseAxes.from_ax(fig=fig) # scatter, bar, box, contour, contourf

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
                except:
                    print(traceback.format_exc(), file=sys.stderr)

                print("")

                fig.clf()
                i += 1
                if i == exit_at - 1: # exit_at must be > 1
                    break
        except KeyboardInterrupt:
            return
        except:
            print(traceback.format_exc(), file=sys.stderr)

        print("First dt: %r" % dt0)
        print("Last  dt: %r" % dt2)
        td = dt2 - dt0
        print("      td: %r" % td.astype('timedelta64[D]'))
        N = i + 1
        print("Number of slides: %d" % N)


    #plt.show()

    print("")
    print("Save file to '%s'" % filename_out)

if __name__ == "__main__":
    main()
