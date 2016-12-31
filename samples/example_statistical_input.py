from windrose import WindroseAxes
from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure(figsize=(12, 8), dpi=80, facecolor='w', edgecolor='w')
ax = WindroseAxes(fig, [0.1, 0.1, 0.8, 0.8], axisbg='w')
fig.add_axes(ax)
windRose = np.loadtxt('amalia_directionally_averaged_speeds.txt')
indexes = np.where(windRose[:, 1] > 0.1)
windDirections = windRose[indexes[0], 0]
windSpeeds = windRose[indexes[0], 1] * 2 / np.sqrt(np.pi) # convert from mean wind speed to weibull scale factor
windFrequencies = windRose[indexes[0], 2]
size  = len(windDirections)
ax.box(windDirections, windSpeeds, frequency=windFrequencies, mean_values=1, bins=[15, 18, 20, 23, 25], nsector=72)
#ax.box(windDirections, [[windSpeeds[i], 2] for i in range(len(windSpeeds))], frequency=windFrequencies, weibull_factors=1, bins=[15, 18, 20, 23, 25], nsector=72)
ax.set_yticklabels([])
plt.show()
