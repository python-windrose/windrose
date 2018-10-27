#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This sample need to be improve to provide
a clean API to output animation

Monthly
python samples/example_animate.py --by M --exit_at 5 --rmax 1000

Daily
python samples/example_animate.py --by D --exit_at 5 --rmax 60

"""

import click

import time
import logging
import traceback

import matplotlib

# matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib.cm as cm

import pandas as pd
import numpy as np

import datetime

from windrose import WindroseAxes, FIGSIZE_DEFAULT, DPI_DEFAULT

logging.Formatter.converter = time.gmtime
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

pd.set_option("max_rows", 10)

S_FIGSIZE_DEFAULT = ",".join(map(str, FIGSIZE_DEFAULT))


def get_by_func(by=None, by_func=None):
    if by is None and by_func is None:
        by = "MS"

    if by in ["year", "yearly", "Y"]:
        return lambda dt: dt.year
    elif by in ["month", "monthly", "MS"]:  # MS: month start
        return lambda dt: (dt.year, dt.month)
    elif by in ["day", "daily", "D"]:
        return lambda dt: (dt.year, dt.month, dt.day)
    elif by is None and by_func is not None:
        return by_func
    else:
        raise NotImplementedError("'%s' is not an allowed 'by' parameter" % by)


def generate(df_all, func, copy=True):
    if copy:
        df_all = df_all.copy()
    df_all["by"] = df_all.index.map(func)
    df = df_all.reset_index().set_index(["by", df_all.index.name])
    for by_val in df.index.levels[0]:
        yield df.loc[by_val]


def count(df_all, func):
    return len(np.unique(df_all.index.map(func)))


@click.command()
@click.option(
    "--filename", default="samples/sample_wind_poitiers.csv", help="Input filename"
)
@click.option("--exit_at", default=0, help="premature exit (int) - must be > 1")
@click.option("--by", default="month", help="Animate by (year, month, day...)")
@click.option("--rmax", default=1000, help="rmax")
@click.option(
    "--filename_out", default="windrose_animation.mp4", help="Output filename"
)
@click.option("--dpi", default=DPI_DEFAULT, help="Dot per inch for plot generation")
@click.option(
    "--figsize",
    default=S_FIGSIZE_DEFAULT,
    help="Figure size x,y - default=%s" % S_FIGSIZE_DEFAULT,
)
@click.option(
    "--fps", default=7, help="Number of frame per seconds for video generation"
)
@click.option("--bins_min", default=0.01, help="Bins minimum value")
@click.option("--bins_max", default=20, help="Bins maximum value")
@click.option("--bins_step", default=2, help="Bins step value")
@click.option("--fontname", default="Courier New", help="Font name")
def main(
    filename,
    exit_at,
    by,
    rmax,
    dpi,
    figsize,
    fps,
    bins_min,
    bins_max,
    bins_step,
    fontname,
    filename_out,
):
    # convert figsize (string like "8,9" to a list of float [8.0, 9.0]
    figsize = figsize.split(",")
    figsize = map(float, figsize)

    by_func = get_by_func(by)

    # Read CSV file to a Pandas DataFrame
    df_all = pd.read_csv(filename)
    df_all["Timestamp"] = pd.to_datetime(df_all["Timestamp"])
    df_all = df_all.set_index("Timestamp")

    df_all.index = df_all.index.tz_localize("UTC").tz_convert("UTC")

    dt_start = df_all.index[0]
    dt_end = df_all.index[-1]

    td = dt_end - dt_start
    Nslides = count(df_all, by_func)
    msg = """Starting
First dt: %s
Last  dt: %s
      td: %s
  Slides: %d""" % (
        dt_start,
        dt_end,
        td,
        Nslides,
    )
    logger.info(msg)

    # Define bins
    bins = np.arange(bins_min, bins_max, bins_step)

    # Create figure
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="w", edgecolor="w")

    # Create a video writer (ffmpeg can create MPEG files)
    FFMpegWriter = matplotlib.animation.writers["ffmpeg"]
    metadata = dict(
        title="windrose",
        artist="windrose",
        comment="""Made with windrose
http://www.github.com/scls19fr/windrose""",
    )
    writer = FFMpegWriter(fps=fps, metadata=metadata)

    dt_start_process = datetime.datetime.now()

    with writer.saving(fig, filename_out, 100):
        try:
            for i, df in enumerate(generate(df_all, by_func)):
                dt1 = df.index[0]
                dt2 = df.index[-1]
                td = dt2 - dt1
                msg = """  Slide %s/%s
    From %s
      to %s
      td %s""" % (
                    i + 1,
                    Nslides,
                    dt1,
                    dt2,
                    td,
                )
                logger.info(msg)
                remaining = Nslides - (i + 1)
                now = datetime.datetime.now()
                td_remaining = (now - dt_start_process) / (i + 1) * remaining
                logger.info(
                    """    Expected
    time: %s
  end at: %s
"""
                    % (td_remaining, now + td_remaining)
                )

                title = "  From %s\n    to %s" % (dt1, dt2)

                try:
                    ax = WindroseAxes.from_ax(
                        fig=fig, rmax=rmax
                    )  # scatter, bar, box, contour, contourf

                    direction = df["direction"].values
                    var = df["speed"].values

                    # ax.scatter(direction, var, alpha=0.2)
                    # ax.set_xlim([-bins[-1], bins[-1]])
                    # ax.set_ylim([-bins[-1], bins[-1]])

                    # ax.bar(direction, var, bins=bins, normed=True, opening=0.8, edgecolor='white')

                    # ax.box(direction, var, bins=bins)

                    # ax.contour(direction, var, cmap=cm.hot, lw=3, bins=bins)

                    ax.contourf(direction, var, bins=bins, cmap=cm.hot)
                    ax.contour(direction, var, bins=bins, colors="black", lw=3)

                    ax.set_legend()

                    # ax = WindAxes.from_ax(fig=fig)  # pdf: probability density function
                    # ax.pdf(var, bins=bins)
                    # ax.set_xlim([0, bins[-1]])
                    # ax.set_ylim([0, 0.4])

                    ax.set_title(title, fontname=fontname)

                    writer.grab_frame()
                except KeyboardInterrupt:
                    break
                except Exception:
                    logger.error(traceback.format_exc())

                fig.clf()
                if i > exit_at - 1 and exit_at != 0:  # exit_at must be > 1
                    break
        except KeyboardInterrupt:
            return
        except Exception:
            logger.error(traceback.format_exc())

        N = i + 1
        logger.info("Number of slides: %d" % N)

    # plt.show()

    logger.info("Save file to '%s'" % filename_out)


if __name__ == "__main__":
    main()
