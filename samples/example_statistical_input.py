import click
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import numpy as np
import os


FILENAME_DEFAULT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "amalia_directionally_averaged_speeds.txt",
)


@click.command()
@click.option("--filename", default=FILENAME_DEFAULT, help="Input filename")
def main(filename):
    fig = plt.figure(figsize=(12, 8), dpi=80, facecolor="w", edgecolor="w")
    ax = WindroseAxes(fig, [0.1, 0.1, 0.8, 0.8], facecolor="w")
    fig.add_axes(ax)
    windRose = np.loadtxt(filename)
    indexes = np.where(windRose[:, 1] > 0.1)
    windDirections = windRose[indexes[0], 0]
    windSpeeds = windRose[indexes[0], 1]
    # windSpeeds = windRose[indexes[0], 1] * 2 / np.sqrt(np.pi)  # convert from mean wind speed to weibull scale factor
    windFrequencies = windRose[indexes[0], 2]
    # size = len(windDirections)
    ax.box(
        windDirections,
        windSpeeds,
        frequency=windFrequencies,
        mean_values=1,
        bins=[15, 18, 20, 23, 25],
        nsector=72,
    )
    # ax.box(windDirections, [[windSpeeds[i], 2] for i in range(len(windSpeeds))], frequency=windFrequencies, weibull_factors=1, bins=[15, 18, 20, 23, 25], nsector=72)
    ax.set_yticklabels([])
    plt.show()


if __name__ == "__main__":
    main()
