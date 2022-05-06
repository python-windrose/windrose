"""Draw windrose (also known as a polar rose plot)"""

from matplotlib.projections import register_projection

from .windrose import D_KIND_PLOT  # noqa
from .windrose import DPI_DEFAULT  # noqa
from .windrose import FIGSIZE_DEFAULT  # noqa
from .windrose import WindAxes  # noqa
from .windrose import WindAxesFactory  # noqa
from .windrose import WindroseAxes  # noqa
from .windrose import clean  # noqa
from .windrose import clean_df  # noqa
from .windrose import plot_windrose  # noqa
from .windrose import plot_windrose_df  # noqa
from .windrose import plot_windrose_np  # noqa
from .windrose import wrbar  # noqa
from .windrose import wrbox  # noqa
from .windrose import wrcontour  # noqa
from .windrose import wrcontourf  # noqa
from .windrose import wrpdf  # noqa
from .windrose import wrscatter  # noqa

register_projection(WindroseAxes)
