"""Draw windrose (also known as a polar rose plot)"""

from matplotlib.projections import register_projection

from .windrose import (
    D_KIND_PLOT,
    DEFAULT_THETA_LABELS,
    DPI_DEFAULT,
    FIGSIZE_DEFAULT,
    WindAxes,
    WindAxesFactory,
    WindroseAxes,
    clean,
    clean_df,
    plot_windrose,
    plot_windrose_df,
    plot_windrose_np,
    wrbar,
    wrbox,
    wrcontour,
    wrcontourf,
    wrpdf,
    wrscatter,
)

__all__ = [
    "D_KIND_PLOT",
    "DEFAULT_THETA_LABELS",
    "DPI_DEFAULT",
    "FIGSIZE_DEFAULT",
    "WindAxes",
    "WindAxesFactory",
    "WindroseAxes",
    "clean",
    "clean_df",
    "plot_windrose",
    "plot_windrose_df",
    "plot_windrose_np",
    "wrbar",
    "wrbox",
    "wrcontour",
    "wrcontourf",
    "wrpdf",
    "wrscatter",
]
register_projection(WindroseAxes)
