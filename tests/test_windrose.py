#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg', warn=False)

from windrose import WindroseAxes
from windrose import new_axes, set_legend, fig_ax
from windrose import pdf
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np

def test_windrose_numpy():

    #Create wind speed and direction variables
    N = 500
    ws = np.random.random(N) * 6
    wd = np.random.random(N) * 360

    #windrose like a stacked histogram with normed (displayed in percent) results
    ax = new_axes()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    set_legend(ax)
    plt.savefig('tests/bar.png')

    #Another stacked histogram representation, not normed, with bins limits
    ax = new_axes()
    ax.box(wd, ws, bins=np.arange(0,8,1))
    set_legend(ax)
    plt.savefig('tests/box.png')

    #A windrose in filled representation, with a controled colormap
    ax = new_axes()
    ax.contourf(wd, ws, bins=np.arange(0,8,1), cmap=cm.hot)
    set_legend(ax)
    plt.savefig('tests/contourf.png')

    #Same as above, but with contours over each filled region...
    ax = new_axes()
    ax.contourf(wd, ws, bins=np.arange(0,8,1), cmap=cm.hot)
    ax.contour(wd, ws, bins=np.arange(0,8,1), colors='black')
    set_legend(ax)
    plt.savefig('tests/contourf2.png')

    #...or without filled regions
    ax = new_axes()
    ax.contour(wd, ws, bins=np.arange(0,8,1), cmap=cm.hot, lw=3)
    set_legend(ax)

    ##print ax._info
    #plt.show()
    plt.savefig('contour.png')

    ax = fig_ax()
    bins = np.arange(0, 30+1, 1)
    bins = bins[1:]
    pdf(wd, ws, bins=bins, ax=ax)
    plt.savefig('pdf.png')

def test_windrose_pandas():
    import pandas as pd
    from windrose import plot_windrose

    N = 500
    ws = np.random.random(N) * 6
    wd = np.random.random(N) * 360
    df = pd.DataFrame({'speed': ws, 'direction': wd})

    plot_windrose(df, kind='contour', bins=np.arange(0.01,8,1), cmap=cm.hot, lw=3)
    plt.savefig('df_contour.png')
