#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from windrose import plot_windrose
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from numpy.random import random
from numpy import arange

df = pd.read_csv("samples/sample_wind_poitiers.csv")
df = df.set_index('Timestamp')
print(df)
plot_windrose(df, kind='contour', bins=arange(0.01,8,1), cmap=cm.hot, lw=3)
plt.show()

#plot_windrose(df, kind='histogram')
#plt.show()
