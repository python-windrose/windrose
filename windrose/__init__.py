#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function  # noqa

from .windrose import (WindAxesFactory, WindroseAxes, WindAxes,  # noqa
    wrcontour, wrcontourf, wrbox, wrbar, wrpdf, wrscatter,  # noqa
    clean, clean_df,  # noqa
    plot_windrose_np, plot_windrose_df, plot_windrose,  # noqa
    FIGSIZE_DEFAULT, DPI_DEFAULT, D_KIND_PLOT)  # noqa

from matplotlib.projections import register_projection
register_projection(WindroseAxes)
