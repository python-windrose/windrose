#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg', warn=False)
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from windrose import WindroseAxes
from windrose import WindAxes
from windrose import FIGSIZE_DEFAULT, DPI_DEFAULT
from windrose import wrbar, wrbox, wrcontour, wrcontourf, wrpdf
from windrose import plot_windrose
from windrose import D_KIND_PLOT

import numpy as np
import pandas as pd

#Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360

df = pd.DataFrame({'speed': ws, 'direction': wd})

def test_windrose_np_mpl_oo():
    bins = np.arange(0, 8, 1)

    #windrose like a stacked histogram with normed (displayed in percent) results
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    plt.savefig('tests/output/oo/bar.png')

    #Another stacked histogram representation, not normed, with bins limits
    ax = WindroseAxes.from_ax()
    ax.box(wd, ws, bins=bins)
    ax.set_legend()
    plt.savefig('tests/output/oo/box.png')

    #A windrose in filled representation, with a controled colormap
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.set_legend()
    plt.savefig('tests/output/oo/contourf.png')

    #Same as above, but with contours over each filled region...
    ax = WindroseAxes.from_ax()
    ax.contourf(wd, ws, bins=bins, cmap=cm.hot)
    ax.contour(wd, ws, bins=bins, colors='black')
    ax.set_legend()
    plt.savefig('tests/output/oo/contourf-contour.png')

    #...or without filled regions
    ax = WindroseAxes.from_ax()
    ax.contour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    ax.set_legend()
    plt.savefig('tests/output/oo/contour.png')

    #print ax._info
    #plt.show()

    ax = WindAxes.from_ax()
    bins = bins[1:]
    ax.pdf(ws, bins=bins)
    plt.savefig('tests/output/oo/pdf.png')

def test_windrose_np_mpl_func():
    bins = np.arange(0, 8, 1)

    wrbar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    plt.savefig('tests/output/func/wrbar.png')

    wrbox(wd, ws, bins=bins)
    plt.savefig('tests/output/func/wrbox.png')
    
    wrcontourf(wd, ws, bins=bins, cmap=cm.hot)
    plt.savefig('tests/output/func/wrcontourf.png')

    #ax = wrcontourf(wd, ws, bins=bin, cmap=cm.hot)
    #wrcontour(wd, ws, bins=np.arange(0, 8, 1), colors='black')
    #plt.savefig('tests/output/func/wrcontourf-contour.png')

    wrcontour(wd, ws, bins=bins, cmap=cm.hot, lw=3)
    plt.savefig('tests/output/func/wrcontour.png')

    wrpdf(ws, bins=bins)
    plt.savefig('tests/output/func/wrpdf.png')

def test_windrose_pandas():
    bins = np.arange(0.01, 8, 1)

    kind = 'bar'
    plot_windrose(df, kind=kind, normed=True, opening=0.8, edgecolor='white')
    plt.savefig('tests/output/df/%s.png' % kind)

    kind = 'box'
    plot_windrose(df, kind=kind, bins=bins)
    plt.savefig('tests/output/df/%s.png' % kind)

    kind = 'contourf'
    plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot)
    plt.savefig('tests/output/df/%s.png' % kind)

    kind = 'contour'
    plot_windrose(df, kind=kind, bins=bins, cmap=cm.hot, lw=3)
    plt.savefig('tests/output/df/%s.png' % kind)

    kind = 'pdf'
    plot_windrose(df, kind=kind, bins=bins)
    plt.savefig('tests/output/df/%s.png' % kind)