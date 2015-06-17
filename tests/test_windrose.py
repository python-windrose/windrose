#!/usr/bin/env python
# -*- coding: utf-8 -*-

from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from numpy.random import random
from numpy import arange

def new_axes():
    fig = plt.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

def set_legend(ax):
    l = ax.legend(borderaxespad=-0.10)
    plt.setp(l.get_texts(), fontsize=8)

def test_windrose():
    #Create wind speed and direction variables
    N = 500
    ws = random(N)*6
    wd = random(N)*360

    #windrose like a stacked histogram with normed (displayed in percent) results
    ax = new_axes()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    set_legend(ax)
    plt.savefig('tests/plot1.png')

    #Another stacked histogram representation, not normed, with bins limits
    ax = new_axes()
    ax.box(wd, ws, bins=arange(0,8,1))
    set_legend(ax)
    plt.savefig('tests/plot2.png')

    #A windrose in filled representation, with a controled colormap
    ax = new_axes()
    ax.contourf(wd, ws, bins=arange(0,8,1), cmap=cm.hot)
    set_legend(ax)
    plt.savefig('tests/plot3.png')

    #Same as above, but with contours over each filled region...
    ax = new_axes()
    ax.contourf(wd, ws, bins=arange(0,8,1), cmap=cm.hot)
    ax.contour(wd, ws, bins=arange(0,8,1), colors='black')
    set_legend(ax)
    plt.savefig('tests/plot4.png')

    #...or without filled regions
    ax = new_axes()
    ax.contour(wd, ws, bins=arange(0,8,1), cmap=cm.hot, lw=3)
    set_legend(ax)

    ##print ax._info
    #plt.show()
    plt.savefig('foo.png')