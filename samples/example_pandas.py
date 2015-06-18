#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from windrose import plot_windrose
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np

df = pd.read_csv("samples/sample_wind_poitiers.csv")
df = df.set_index('Timestamp')
#print(df)
#plot_windrose(df, kind='contour', bins=arange(0.01,8,1), cmap=cm.hot, lw=3)
#plt.show()

#plot_windrose(df, kind='histogram')
#plt.show()

bins = np.arange(0,30+1,1)
bins = bins[1:]

#fig, ax = plt.subplots(figsize=(8, 8), dpi=80)
res = plot_windrose(df, kind='pdf', bins=bins)
print(res)
plt.show()
