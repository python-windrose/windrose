#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
sample using "by" keyword
"""

import click

# import matplotlib
# matplotlib.use("Agg")
# import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
import pandas as pd

from windrose import WindroseAxes, FIGSIZE_DEFAULT, DPI_DEFAULT


class AxCollection(object):
    def __init__(self, fig=None, *args, **kwargs):
        if fig is None:
            self.fig = plt.figure(
                figsize=FIGSIZE_DEFAULT, dpi=DPI_DEFAULT, facecolor="w", edgecolor="w"
            )
        else:
            self.fig = fig

    def animate(self):
        pass

    def show(self):
        pass


class Layout(object):
    """
    Inspired from PdfPages
        https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/backend_pdf.py - PdfPages
        http://matplotlib.org/api/backend_pdf_api.html
        http://matplotlib.org/examples/pylab_examples/multipage_pdf.html

    Inspired also from FFMpegWriter
        http://matplotlib.org/examples/animation/moviewriter.html
        https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/animation.py
        MovieWriter
    """

    def __init__(self, ncols=4, nrows=6, nsheets=1):
        self.ncols = ncols
        self.nrows = nrows
        self.nsheets = nsheets

        self._resize()
        self._i = 0

    @property
    def fig(self):
        return self._array_fig

    def _resize(self):
        # self._array_ax = np.empty((self.nsheets, self.nrows, self.ncols), dtype=object)
        self._array_ax = np.empty(self.nsheets, dtype=object)
        # self._array_ax.fill(None)

        self._array_fig = np.empty(self.nsheets, dtype=object)
        # self._array_fig.fill(None)

        for i in range(self.nsheets):
            fig, axs = plt.subplots(nrows=self.nrows, ncols=self.ncols)
            # print(fig, axs)
            self._array_fig[i] = fig
            self._array_ax[i] = axs

    def __repr__(self):
        s = """<Layout
  cols: %s
  rows: %s
  sheets: %s
>""" % (
            self.ncols,
            self.nrows,
            self.nsheets,
        )
        return s

    def __enter__(self, *args, **kwargs):
        print("enter %s %s" % (args, kwargs))
        return self

    def __exit__(self, type, value, traceback):
        # print("exit %s %s" % (args, kwargs))
        print("exit %s %s %s" % (type, value, traceback))
        # print("exit")
        self.close()

    def close(self):
        print("close")

    def saveax(self):
        print("saveax")
        self._i += 1


class NormalLayout(Layout):
    def __init__(self):
        super(NormalLayout, self).__init__()


S_FIGSIZE_DEFAULT = ",".join(map(str, FIGSIZE_DEFAULT))


def by_func_yearly(dt):
    return dt.year


def by_func_monthly(dt):
    return dt.year, dt.month


def by_func_daily(dt):
    return dt.year, dt.month, dt.day


@click.command()
@click.option(
    "--filename", default="samples/sample_wind_poitiers.csv", help="Input filename"
)
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
def main(filename, dpi, figsize, fps, bins_min, bins_max, bins_step, filename_out):
    # convert figsize (string like "8,9" to a list of float [8.0, 9.0]
    figsize = figsize.split(",")
    figsize = map(float, figsize)

    # Read CSV file to a Pandas DataFrame
    df_all = pd.read_csv(filename)
    df_all["Timestamp"] = pd.to_datetime(df_all["Timestamp"])
    df_all = df_all.set_index("Timestamp")
    df_all.index = df_all.index.tz_localize("UTC").tz_convert("UTC")
    # df_all = df_all.iloc[-10000:,:]
    df_all = df_all.ix["2011-07-01":"2011-12-31"]

    # Get Numpy arrays from DataFrame
    direction_all = df_all["direction"].values
    var_all = df_all["speed"].values
    index_all = df_all.index.to_datetime()  # Fixed: .values -> to_datetime()
    by_all = df_all.index.map(by_func_monthly)
    by_unique = np.unique(by_all)
    print(by_unique)

    (ncols, nrows, nsheets) = (4, 3, 2)  # noqa
    # layout = Layout(4, 3, 2) # ncols, nrows, nsheets
    # layout = Layout(ncols, nrows, nsheets)

    # layout = Layout(4, 6, 1)
    # layout.save(ax)
    # layout.to_pdf("filename.pdf")
    # layout.to_video("filename.mp4")

    # fig, ax = plt.subplots(nrows=2, ncols=3)

    # with Layout(4, 6, 1) as layout:
    #     print(layout)
    #     #layout.save(ax)

    def tuple_position(i, ncols, nrows):
        i_sheet, sheet_pos = divmod(i, ncols * nrows)
        i_row, i_col = divmod(sheet_pos, ncols)
        return i_sheet, i_row, i_col

    def position_from_tuple(t, ncols, nrows):
        i_sheet, i_row, i_col = t
        return i_sheet * ncols * nrows + i_row * ncols + i_col

    assert tuple_position(0, ncols, nrows) == (0, 0, 0)
    assert tuple_position(1, ncols, nrows) == (0, 0, 1)
    assert tuple_position(2, ncols, nrows) == (0, 0, 2)
    assert tuple_position(3, ncols, nrows) == (0, 0, 3)
    assert tuple_position(4, ncols, nrows) == (0, 1, 0)
    assert tuple_position(5, ncols, nrows) == (0, 1, 1)
    assert tuple_position(6, ncols, nrows) == (0, 1, 2)
    assert tuple_position(7, ncols, nrows) == (0, 1, 3)
    assert tuple_position(8, ncols, nrows) == (0, 2, 0)
    assert tuple_position(9, ncols, nrows) == (0, 2, 1)
    assert tuple_position(10, ncols, nrows) == (0, 2, 2)
    assert tuple_position(11, ncols, nrows) == (0, 2, 3)
    assert tuple_position(12, ncols, nrows) == (1, 0, 0)
    assert tuple_position(13, ncols, nrows) == (1, 0, 1)
    assert tuple_position(14, ncols, nrows) == (1, 0, 2)
    assert tuple_position(15, ncols, nrows) == (1, 0, 3)
    assert tuple_position(16, ncols, nrows) == (1, 1, 0)
    assert tuple_position(17, ncols, nrows) == (1, 1, 1)

    assert position_from_tuple((0, 0, 0), ncols, nrows) == 0
    assert position_from_tuple((1, 0, 0), ncols, nrows) == ncols * nrows
    assert position_from_tuple((2, 0, 0), ncols, nrows) == 2 * ncols * nrows
    assert position_from_tuple((1, 0, 1), ncols, nrows) == ncols * nrows + 1
    assert position_from_tuple((1, 1, 1), ncols, nrows) == ncols * nrows + ncols + 1
    assert position_from_tuple((1, 2, 3), ncols, nrows) == ncols * nrows + 2 * ncols + 3

    for i in range(20):
        t = tuple_position(i, ncols, nrows)
        assert position_from_tuple(t, ncols, nrows) == i

    # layout = NormalLayout()

    # with layout.append() as ax:
    #     pass
    # layout.show()

    # Define bins
    bins = np.arange(bins_min, bins_max, bins_step)

    for by_value in by_unique:
        # by_value = (2011, 5)

        # mask = (by == by_value).all(axis=1)
        # ToFix: see http://stackoverflow.com/questions/32005403/boolean-indexing-with-numpy-array-and-tuples

        mask = (pd.Series(by_all) == by_value).values

        # print(mask)

        index = index_all[mask]
        var = var_all[mask]
        direction = direction_all[mask]

        # Create figure
        # fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='w', edgecolor='w')

        # Same as above, but with contours over each filled region...
        ax = WindroseAxes.from_ax()
        ax.contourf(direction, var, bins=bins, cmap=cm.hot)
        ax.contour(direction, var, bins=bins, colors="black")
        fontname = "Courier"
        # title = by_value
        dt1 = index[0]
        dt2 = index[-1]
        # dt1 = df.index[mask][0]
        # dt2 = df.index[mask][-1]
        # td = dt2 - dt1
        title = "From %s\n  to %s" % (dt1, dt2)

        ax.set_title(title, fontname=fontname)
        ax.set_legend()

        plt.show()

    # time.sleep(10)

    # print("Save file to '%s'" % filename_out)


if __name__ == "__main__":
    main()
