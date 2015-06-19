#!/usr/bin/env python
# -*- coding: utf-8 -*-

from windrose import WindroseAxes
from windrose import new_axes, set_legend
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np

#Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360

#windrose like a stacked histogram with normed (displayed in percent) results
ax = new_axes()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
set_legend(ax)

#Another stacked histogram representation, not normed, with bins limits
ax = new_axes()
ax.box(wd, ws, bins=np.arange(0, 8, 1))
set_legend(ax)

#A windrose in filled representation, with a controled colormap
ax = new_axes()
ax.contourf(wd, ws, bins=np.arange(0, 8, 1), cmap=cm.hot)
set_legend(ax)

#Same as above, but with contours over each filled region...
ax = new_axes()
ax.contourf(wd, ws, bins=np.arange(0, 8, 1), cmap=cm.hot)
ax.contour(wd, ws, bins=np.arange(0, 8, 1), colors='black')
set_legend(ax)

#...or without filled regions
ax = new_axes()
ax.contour(wd, ws, bins=np.arange(0, 8, 1), cmap=cm.hot, lw=3)
set_legend(ax)

##print ax._info
plt.show()

    
    