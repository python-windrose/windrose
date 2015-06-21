#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
This sample need to be improve to provide
a clean API to output animation
"""

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

def main():
    df = pd.read_csv("samples/sample_wind_poitiers.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.set_index('Timestamp')
    #df = df.iloc[-10000:,:]
    direction = df['direction'].values
    var = df['speed'].values
    index = df.index.values

    bins = np.arange(0.01, 8, 1)

    fig = plt.figure(figsize=FIGSIZE_DEFAULT, dpi=DPI_DEFAULT, facecolor='w', edgecolor='w')
    #ax.scatter(direction, var, alpha=0.2)


    FFMpegWriter = mpl.animation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib',
            comment='Movie support!')
    writer = FFMpegWriter(fps=15, metadata=metadata)

    size = 36 * 4
    offset = 3 + 6 * 6 + 24 * 6 * 365 * 2 - 24 * 6 * 65

    print("First dt: %s" % index[offset])

    dt2 = None
    i = 0
    with writer.saving(fig, "windrose_animation_bar.mp4", 100):
        #for i in range(1000): # 100
        try:
            while True:
                ax = WindroseAxes.from_ax(fig=fig)

                print("Processing %d" % (i + 1))
                i1 = offset + i*size
                i2 = offset + (i+1)*size + 1

                index_tmp = index[i1:i2]
                dt1 = index_tmp[0]
                dt2 = index_tmp[-1]
                td = dt2 - dt1
                title = """  From %s
    to %s""" % (dt1, dt2)
                print(title)
                print("""    td %r""" % td.astype('timedelta64[m]'))
    
                try:
                    wd = direction[i1:i2]
                    ws = var[i1:i2]

                    #ax.scatter(wd, ws, alpha=0.2)

                    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')

                    #ax.box(wd, ws, bins=bins)

                    #ax.contour(wd, ws, cmap=cm.hot, lw=3, bins=bins)

                    #ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
                    #ax.contour(wd, ws, bins=bins, colors='black')

                    ax.set_legend()

                    ax.set_title(title, fontname="Courier New")
                    writer.grab_frame()
                except:
                    print(traceback.format_exc(), file=sys.stderr)

                print("")

                fig.clf()
                i += 1
        except:
            print(traceback.format_exc(), file=sys.stderr)

        print("Last  dt: %s" % dt2)


    #plt.show()

if __name__ == "__main__":
    main()
