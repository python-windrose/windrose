"""Windrose for matplotlib"""

import locale
import random

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.projections.polar import PolarAxes
from numpy import histogram2d

ZBASE = -1000  # The starting zorder for all drawing, negative to have the grid on
VAR_DEFAULT = "speed"
DIR_DEFAULT = "direction"
FIGSIZE_DEFAULT = (8, 8)
DPI_DEFAULT = 80
DEFAULT_THETA_LABELS = ["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"]


def _copy_docstring(source):
    """

    Copy the docstring from another function.
    Implemented according to: https://github.com/matplotlib/matplotlib/blob/b5ac96a8980fdb9e59c9fb649e0714d776e26701/lib/matplotlib/_docstring.py#L86-L92

    """  # noqa: E501

    def inner(target):
        if source.__doc__ is not None:
            target.__doc__ = source.__doc__
        return target

    return inner


class WindAxesFactory:
    """

    Factory class to create WindroseAxes or WindAxes

    """

    @staticmethod
    def create(typ, ax=None, *args, **kwargs):
        """

        Create

        Mandatory:

        Parameters
        ----------
        typ : string, 'windroseaxes' or 'windaxes'
            Type of axes to create
                * windroseaxes : a WindroseAxes axe
                * windaxe : a WindAxes axe

        ax : matplotlib.Axes, optional
            A matplotlib axe

        """
        typ = typ.lower()
        d = {"windroseaxes": WindroseAxes, "windaxes": WindAxes}
        if typ in d.keys():
            cls = d[typ]
            if isinstance(ax, cls):
                return ax
            else:
                ax = cls.from_ax(ax, *args, **kwargs)
                return ax
        else:
            raise NotImplementedError(f"typ={typ!r} but it might be in {d.keys()}")


class WindroseAxes(PolarAxes):
    """

    Create a windrose axes

    """

    name = "windrose"

    def __init__(self, *args, **kwargs):
        """
        See Axes base class for args and kwargs documentation

        Other kwargs are:

        theta_labels : default ["E", "N-E", "N", "N-W", "W", "S-W", "S", "S-E"]
            Labels for theta coordinate
        """

        # Uncomment to have the possibility to change the resolution directly
        # when the instance is created
        # self.RESOLUTION = kwargs.pop('resolution', 100)
        self.rmax = kwargs.pop("rmax", None)
        self.theta_labels = kwargs.pop("theta_labels", DEFAULT_THETA_LABELS)

        PolarAxes.__init__(self, *args, **kwargs)
        self.set_aspect("equal", adjustable="box", anchor="C")
        self.radii_angle = 67.5
        self.clear()

    @staticmethod
    def from_ax(
        ax=None,
        fig=None,
        rmax=None,
        figsize=FIGSIZE_DEFAULT,
        rect=None,
        *args,
        **kwargs,
    ):
        """
        Return a WindroseAxes object for the figure `fig`.
        """
        if ax is None:
            if fig is None:
                fig = plt.figure(
                    figsize=figsize,
                    dpi=DPI_DEFAULT,
                    facecolor="w",
                    edgecolor="w",
                )
            if rect is None:
                rect = [0.1, 0.1, 0.8, 0.8]
            ax = WindroseAxes(fig, rect, *args, **kwargs)
            fig.add_axes(ax)
            return ax
        else:
            return ax

    def clear(self):
        """
        Clear the current axes
        """
        PolarAxes.clear(self)

        self.theta_angles = np.arange(0, 360, 45)
        self.set_thetagrids(angles=self.theta_angles, labels=self.theta_labels)

        self._info = {"dir": [], "bins": [], "table": []}

        self.patches_list = []

        self.calm_count = None

    def _colors(self, cmap, n):
        """
        Returns a list of n colors based on the colormap cmap

        """
        return [cmap(i) for i in np.linspace(0.0, 1.0, n)]

    def set_radii_angle(self, **kwargs):
        """
        Set the radii labels angle
        """

        kwargs.pop("labels", None)
        angle = kwargs.pop("angle", None)
        if angle is None:
            angle = self.radii_angle
        self.radii_angle = angle
        N = 5
        rmax = self.get_rmax()
        radii = np.linspace(0, rmax, N + 1)
        if rmax % N == 0:
            fmt = "%d"
        else:
            fmt = "%.1f"
        radii_labels = [fmt % r for r in radii]
        # radii_labels[0] = ""  # Removing label 0
        self.set_rgrids(
            radii=radii[1:],
            labels=radii_labels[1:],
            angle=self.radii_angle,
            **kwargs,
        )

    def _update(self):
        if not self.rmax:
            self.rmax = np.max(np.sum(self._info["table"], axis=0))
        calm_count = self.calm_count or 0
        self.set_rmax(rmax=self.rmax + calm_count)
        self.set_radii_angle(angle=self.radii_angle)

    def legend(self, loc="lower left", decimal_places=1, units=None, **kwargs):
        """
        Sets the legend location and her properties.

        Parameters
        ----------
        loc : int, string or pair of floats, default: 'lower left'
            see :obj:`matplotlib.pyplot.legend`.

        decimal_places : int, default 1
            The decimal places of the formatted legend

        units: str, default None

        Other Parameters
        ----------------
        isaxes : boolean, default True
            whether this is an axes legend
        prop : FontProperties(size='smaller')
            the font property
        borderpad : float
            the fractional whitespace inside the legend border
        shadow : boolean
            if True, draw a shadow behind legend
        labelspacing : float, 0.005
            the vertical space between the legend entries
        handlelenght : float, 0.05
            the length of the legend lines
        handletextsep : float, 0.02
            the space between the legend line and legend text
        borderaxespad : float, 0.02
            the border between the axes and legend edge
        kwarg
            Every other kwarg argument supported by
            :obj:`matplotlib.pyplot.legend`
        """

        def get_handles():
            handles = []
            for p in self.patches_list:
                if isinstance(p, mpl.patches.Polygon) or isinstance(
                    p,
                    mpl.patches.Rectangle,
                ):
                    color = p.get_facecolor()
                elif isinstance(p, mpl.lines.Line2D):
                    color = p.get_color()
                else:
                    raise AttributeError("Can't handle patches")
                handles.append(
                    mpl.patches.Rectangle(
                        (0, 0),
                        0.2,
                        0.2,
                        facecolor=color,
                        edgecolor="black",
                    ),
                )
            return handles

        def get_labels(decimal_places=1, units=None):
            digits = np.copy(self._info["bins"]).tolist()
            if not digits:
                return ""
            digits[-1] = digits[-2]
            digits = [f"{label:.{decimal_places}f}" for label in digits]
            fmt = "[{} : {}"
            if locale.getlocale()[0] in ["fr_FR"]:
                fmt += "["
            else:
                fmt += ")"

            if units:
                fmt += " " + units

            labels = [
                fmt.format(digits[k], digits[k + 1]) for k in range(len(digits) - 1)
            ]
            labels[-1] = f">{digits[-1]}"
            return labels

        kwargs.pop("labels", None)
        kwargs.pop("handles", None)

        handles = get_handles()
        labels = get_labels(decimal_places, units)
        self.legend_ = mpl.legend.Legend(self, handles, labels, loc=loc, **kwargs)
        return self.legend_

    def set_legend(self, **pyplot_arguments):
        if "borderaxespad" not in pyplot_arguments:
            pyplot_arguments["borderaxespad"] = -0.10
        legend = self.legend(**pyplot_arguments)
        plt.setp(legend.get_texts(), fontsize=8)
        return legend

    def _init_plot(self, direction, var, **kwargs):
        """
        Internal method used by all plotting commands

        Parameters
        ----------
        direction : 1D array,
            directions the wind blows from, North centred
        var : 1D array,
            values of the variable to compute. Typically the wind speeds

        Other Parameters
        ----------------
        normed : boolean, default False
        blowto : boolean, default False
        colors : str or list of str, default None
            The colors of the plot.
        cmap : color map
            A :obj:`matplotlib.cm` colormap for the plot.
            Warning! It overrides `colors`.
        weibull_factors :
        mean_values :
        frequency :
        calm_limit : float, default None
        kwarg
            Any argument accepted by :obj:`matplotlib.pyplot.plot`.
        """

        normed = kwargs.pop("normed", False)
        blowto = kwargs.pop("blowto", False)

        # Calm condition, mask data if needed
        calm_limit = kwargs.pop("calm_limit", None)
        total = len(var)
        if calm_limit is not None:
            mask = var > calm_limit
            self.calm_count = len(var) - np.count_nonzero(mask)
            if normed:
                self.calm_count = self.calm_count * 100 / len(var)
            var = var[mask]
            direction = direction[mask]

        # if weibull factors are entered overwrite direction and var
        if "weibull_factors" in kwargs or "mean_values" in kwargs:
            if "weibull_factors" in kwargs and "mean_values" in kwargs:
                raise TypeError("cannot specify both weibull_factors and mean_values")
            statistic_type = "unset"
            if "weibull_factors" in kwargs:
                statistic_type = "weibull"
                val = kwargs.pop("weibull_factors")
            elif "mean_values" in kwargs:
                statistic_type = "mean"
                val = kwargs.pop("mean_values")
            if val:
                if "frequency" not in kwargs:
                    raise TypeError(
                        "specify 'frequency' argument for statistical input",
                    )
                windFrequencies = kwargs.pop("frequency")
                if len(windFrequencies) != len(direction) or len(direction) != len(var):
                    if len(windFrequencies) != len(direction):
                        raise TypeError("len(frequency) != len(direction)")
                    elif len(direction) != len(var):
                        raise TypeError("len(frequency) != len(direction)")
                windSpeeds = []
                windDirections = []
                for dbin in range(len(direction)):
                    for _ in range(int(windFrequencies[dbin] * 10000)):
                        if statistic_type == "weibull":
                            windSpeeds.append(
                                random.weibullvariate(var[dbin][0], var[dbin][1]),
                            )
                        elif statistic_type == "mean":
                            windSpeeds.append(
                                random.weibullvariate(
                                    var[dbin] * 2 / np.sqrt(np.pi),
                                    2,
                                ),
                            )
                        windDirections.append(direction[dbin])
                var, direction = windSpeeds, windDirections

        # self.clear()
        kwargs.pop("zorder", None)

        # Init of the bins array if not set
        bins = kwargs.pop("bins", None)
        if bins is None:
            bins = np.linspace(np.min(var), np.max(var), 6)
        if isinstance(bins, (list, tuple, np.ndarray)):
            if len(bins) > 0 and bins[0] > np.min(var) and not calm_limit:
                raise ValueError(
                    f"the first value provided in bins must be less than or equal "
                    f"to the minimum value of the wind speed data. "
                    f"Did you mean: bins={(0, *bins)!r} ? "
                    f"If you want to exclude values below a certain threshold, "
                    f"try setting calm_limit={min(bins)}.",
                )
            elif len(bins) > 0 and calm_limit is not None and min(bins) < calm_limit:
                raise ValueError(
                    f"the lowest value in bins must be >= {calm_limit} (=calm_limits)",
                )
        if isinstance(bins, int):
            bins = np.linspace(np.min(var), np.max(var), bins)
        bins = np.asarray(bins)
        nbins = len(bins)

        if np.isnan(bins).any():
            raise ValueError(
                "Could not compute the bins due to the presence of NaNs in "
                "either the bins provided or the original data.",
            )

        # Number of sectors
        nsector = kwargs.pop("nsector", None)
        if nsector is None:
            nsector = 16

        sector_offset = kwargs.get("sectoroffset", 0)

        # Sets the colors table based on the colormap or the "colors" argument
        colors = kwargs.pop("colors", None)
        cmap = kwargs.pop("cmap", None)
        if colors is not None:
            if isinstance(colors, str):
                colors = [colors] * nbins
            if isinstance(colors, (tuple, list)):
                if len(colors) != nbins:
                    raise ValueError("colors and bins must have same length")
        else:
            if cmap is None:
                cmap = plt.get_cmap()
            colors = self._colors(cmap, nbins)

        # Building the angles list
        angles = np.arange(0, -2 * np.pi, -2 * np.pi / nsector) + np.pi / 2

        # Set the global information dictionary
        self._info["dir"], self._info["bins"], self._info["table"] = histogram(
            direction,
            var,
            bins,
            nsector,
            total,
            sector_offset,
            normed,
            blowto,
        )

        return bins, nbins, nsector, colors, angles, kwargs

    def _calm_circle(self):
        """Draw the calm centered circle"""
        if self.calm_count and self.calm_count > 0:
            self.set_rorigin(-(np.sqrt(self.calm_count / np.pi)))

    def contour(self, direction, var, **kwargs):
        """
        Plot a windrose in linear mode. For each var bins, a line will be
        draw on the axes, a segment between each sector (center to center).
        Each line can be formatted (color, width, ...) like with standard plot
        pylab command.

        Parameters
        ----------
        direction : 1D array
            directions the wind blows from, North centred
        var : 1D array
            values of the variable to compute. Typically the wind speeds.

        Other Parameters
        ----------------
        nsector : integer, optional
            number of sectors used to compute the windrose table. If not set,
            nsector=16, then each sector will be 360/16=22.5°, and the
            resulting computed table will be aligned with the cardinals points.
        bins : 1D array or integer, optional
            number of bins, or a sequence of bins variable. If not set, bins=6,
            then bins=linspace(min(var), max(var), 6)
        blowto : bool, optional
            If True, the windrose will be pi rotated, to show where the wind
            blow to (useful for pollutant rose).
        colors : string or tuple, optional
            one string color ('k' or 'black'), in this case all bins will be
            plotted in this color; a tuple of matplotlib color args (string,
            float, rgb, etc), different levels will be plotted in different
            colors in the order specified.
        cmap : a cm Colormap instance from :obj:`matplotlib.cm`, optional
            if cmap == None and colors == None, a default Colormap is used.
        calm_limit : float, optional
            Calm limit for the var parameter. If not None, a centered red
            circle will be draw for representing the calms occurrences and all
            data below this value will be removed from the computation.

        others kwargs
            Any supported argument of :obj:`matplotlib.pyplot.plot`

        """
        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(
            direction,
            var,
            **kwargs,
        )

        # closing lines
        angles = np.hstack((angles, angles[-1] - 2 * np.pi / nsector))
        vals = np.hstack(
            (
                self._info["table"],
                np.reshape(
                    self._info["table"][:, 0],
                    (self._info["table"].shape[0], 1),
                ),
            ),
        )

        self._calm_circle()
        origin = 0
        for i in range(nbins):
            val = vals[i, :] + origin
            origin += vals[i, :]
            zorder = ZBASE + nbins - i
            patch = self.plot(angles, val, color=colors[i], zorder=zorder, **kwargs)
            self.patches_list.extend(patch)
        self._update()

    def contourf(self, direction, var, **kwargs):
        """
        Plot a windrose in filled mode. For each var bins, a line will be
        draw on the axes, a segment between each sector (center to center).
        Each line can be formatted (color, width, ...) like with standard plot
        pylab command.

        Parameters
        ----------
        direction : 1D array
            directions the wind blows from, North centred
        var : 1D array
            values of the variable to compute. Typically the wind speeds

        Other Parameters
        ----------------
        nsector: integer, optional
            number of sectors used to compute the windrose table. If not set,
            nsector=16, then each sector will be 360/16=22.5°, and the
            resulting computed table will be aligned with the cardinals points.
        bins : 1D array or integer, optional
            number of bins, or a sequence of bins variable. If not set, bins=6,
            then bins=linspace(min(`var`), max(`var`), 6)
        blowto : bool, optional
            If True, the windrose will be pi rotated, to show where the wind
            blow to (useful for pollutant rose).
        colors : string or tuple, optional
            one string color ('k' or 'black'), in this case all bins will be
            plotted in this color; a tuple of matplotlib color args (string,
            float, rgb, etc), different levels will be plotted in different
            colors in the order specified.
        cmap : a cm Colormap instance from :obj:`matplotlib.cm`, optional
            if cmap == None and colors == None, a default Colormap is used.
        calm_limit : float, optional
            Calm limit for the var parameter. If not None, a centered red
            circle will be draw for representing the calms occurrences and all
            data below this value will be removed from the computation.

        others kwargs
            Any supported argument of :obj:`matplotlib.pyplot.plot`
        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(
            direction,
            var,
            **kwargs,
        )
        kwargs.pop("facecolor", None)
        kwargs.pop("edgecolor", None)

        # closing lines
        angles = np.hstack((angles, angles[-1] - 2 * np.pi / nsector))
        vals = np.hstack(
            (
                self._info["table"],
                np.reshape(
                    self._info["table"][:, 0],
                    (self._info["table"].shape[0], 1),
                ),
            ),
        )
        self._calm_circle()
        origin = 0
        for i in range(nbins):
            val = vals[i, :] + origin
            origin += vals[i, :]
            zorder = ZBASE + nbins - i
            patch = self.fill(
                np.append(angles, 0),
                np.append(val, 0),
                facecolor=colors[i],
                edgecolor=colors[i],
                zorder=zorder,
                **kwargs,
            )
            self.patches_list.extend(patch)
        self._update()

    def bar(self, direction, var, **kwargs):
        """
        Plot a windrose in bar mode. For each var bins and for each sector,
        a colored bar will be draw on the axes.

        Parameters
        ----------
        direction : 1D array
            directions the wind blows from, North centred
        var : 1D array
            values of the variable to compute. Typically the wind speeds.

        Other Parameters
        ----------------
        nsector : integer, optional
            number of sectors used to compute the windrose table. If not set,
            nsector=16, then each sector will be 360/16=22.5°, and the
            resulting computed table will be aligned with the cardinals points.
        sectoroffset: float, optional
            the offset for the sectors between [-180/nsector, 180/nsector].
            By default, the offset is zero, and the first sector is
            [-360/nsector/2, 360/nsector/2] or [-11.25, 11.25] for nsector=16.
            If offset is non-zero, the first sector will be
            [-360/nsector + offset, 360/nsector + offset] and etc.
        bins : 1D array or integer, optional
            number of bins, or a sequence of bins variable. If not set, bins=6
            between min(`var`) and max(`var`).
        blowto : bool, optional.
            if True, the windrose will be pi rotated, to show where the wind
            blow to (useful for pollutant rose).
        colors : string or tuple, optional
            one string color ('k' or 'black'), in this case all bins will be
            plotted in this color; a tuple of matplotlib color args (string,
            float, rgb, etc), different levels will be plotted
            in different colors in the order specified.
        cmap : a cm Colormap instance from :obj:`matplotlib.cm`, optional.
            if cmap == None and colors == None, a default Colormap is used.
        edgecolor : string, optional
            The string color each edge box will be plotted.
            Default : no edgecolor
        opening : float, optional
            between 0.0 and 1.0, to control the space between each sector (1.0
            for no space)
        calm_limit : float, optional
            Calm limit for the var parameter. If not None, a centered red
            circle will be draw for representing the calms occurrences and all
            data below this value will be removed from the computation.

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(
            direction,
            var,
            **kwargs,
        )
        kwargs.pop("facecolor", None)
        edgecolor = kwargs.pop("edgecolor", None)
        if edgecolor is not None:
            if not isinstance(edgecolor, str):
                raise ValueError("edgecolor must be a string color")
        opening = kwargs.pop("opening", None)
        if opening is None:
            opening = 0.8
        dtheta = 2 * np.pi / nsector
        opening = dtheta * opening

        self._calm_circle()

        # sector offset in radius
        sector_offset = kwargs.pop("sectoroffset", 0) / 180 * np.pi

        for j in range(nsector):
            origin = 0
            for i in range(nbins):
                if i > 0:
                    origin += self._info["table"][i - 1, j]
                val = self._info["table"][i, j]
                zorder = ZBASE + nbins - i
                patch = mpl.patches.Rectangle(
                    (angles[j] - opening / 2 - sector_offset, origin),
                    opening,
                    val,
                    facecolor=colors[i],
                    edgecolor=edgecolor,
                    zorder=zorder,
                    **kwargs,
                )
                # needed so the the line of the rectangle becomes curved
                patch.get_path()._interpolation_steps = 100
                self.add_patch(patch)
                if j == 0:
                    self.patches_list.append(patch)
        self._update()

    def box(self, direction, var, **kwargs):
        """
        Plot a windrose in proportional box mode. For each var bins and for
        each sector, a colored box will be draw on the axes.

        Parameters
        ----------
        direction : 1D array
            directions the wind blows from, North centred
        var : 1D array
            values of the variable to compute. Typically the wind speeds

        Other Parameters
        ----------------
        nsector: integer, optional
            number of sectors used to compute the windrose table. If not set,
            nsector=16, then each sector will be 360/16=22.5°, and the
            resulting computed table will be aligned with the cardinals points.
        sectoroffset: float, optional
            the offset for the sectors. By default, the offsect is zero, and
            the first sector is [-360/nsector, 360/nsector] or [-11.25, 11.25]
            for nsector=16. If offset is non-zero, the first sector will be
            [-360/nsector + offset, 360/nsector + offset] and etc.
        bins : 1D array or integer, optional
            number of bins, or a sequence of bins variable. If not set, bins=6
            between min(`var`) and max(`var`).
        blowto : bool, optional
            If True, the windrose will be pi rotated, to show where the wind
            blow to (useful for pollutant rose).
        colors : string or tuple, optional
            one string color ('k' or 'black'), in this case all bins will be
            plotted in this color; a tuple of matplotlib color args (string,
            float, rgb, etc), different levels will be plotted in different
            colors in the order specified.
        cmap : a cm Colormap instance from :obj:`matplotlib.cm`, optional
            if cmap == None and colors == None, a default Colormap is used.
        edgecolor : string, optional
            The string color each edge bar will be plotted.  Default : no
            edgecolor
        calm_limit : float, optional
            Calm limit for the var parameter. If not None, a centered red
            circle will be draw for representing the calms occurrences and all
            data below this value will be removed from the computation.

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(
            direction,
            var,
            **kwargs,
        )
        kwargs.pop("facecolor", None)
        edgecolor = kwargs.pop("edgecolor", None)
        if edgecolor is not None:
            if not isinstance(edgecolor, str):
                raise ValueError("edgecolor must be a string color")
        opening = np.linspace(0.0, np.pi / 16, nbins)

        self._calm_circle()

        # sector offset in radius
        sector_offset = kwargs.pop("sectoroffset", 0) / 180 * np.pi

        for j in range(nsector):
            origin = 0
            for i in range(nbins):
                if i > 0:
                    origin += self._info["table"][i - 1, j]
                val = self._info["table"][i, j]
                zorder = ZBASE + nbins - i
                patch = mpl.patches.Rectangle(
                    (angles[j] - opening[i] / 2 - sector_offset, origin),
                    opening[i],
                    val,
                    facecolor=colors[i],
                    edgecolor=edgecolor,
                    zorder=zorder,
                    **kwargs,
                )
                # needed so the the line of the rectangle becomes curved
                patch.get_path()._interpolation_steps = 100
                self.add_patch(patch)
                if j == 0:
                    self.patches_list.append(patch)
        self._update()


class WindAxes(mpl.axes.Subplot):
    def __init__(self, *args, **kwargs):
        """
        See Axes base class for args and kwargs documentation
        """
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_ax(ax=None, fig=None, figsize=FIGSIZE_DEFAULT, *args, **kwargs):
        if ax is None:
            if fig is None:
                fig = plt.figure(figsize=figsize, dpi=DPI_DEFAULT)
            ax = WindAxes(fig, 1, 1, 1, *args, **kwargs)
            fig.add_axes(ax)
            return ax
        else:
            return ax

    def pdf(
        self,
        var,
        bins=None,
        Nx=100,
        bar_color="b",
        plot_color="g",
        Nbins=10,
        *args,
        **kwargs,
    ):
        """
        Draw probability density function and return Weibull distribution
        parameters
        """
        import scipy.stats

        if bins is None:
            bins = np.linspace(0, np.max(var), Nbins)
        hist, bins = np.histogram(var, bins=bins, density=True)
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        self.bar(center, hist, align="center", width=width, color=bar_color)
        params = scipy.stats.exponweib.fit(var, floc=0, f0=1)
        x = np.linspace(0, bins[-1], Nx)
        self.plot(x, scipy.stats.exponweib.pdf(x, *params), color=plot_color)
        return (self, params)


def histogram(
    direction,
    var,
    bins,
    nsector,
    total,
    sectoroffset=0,
    normed=False,
    blowto=False,
):
    """
    Returns an array where, for each sector of wind
    (centred on the north), we have the number of time the wind comes with a
    particular var (speed, pollutant concentration, ...).

    Parameters
    ----------
    direction : 1D array
        directions the wind blows from, North centred
    var : 1D array
        values of the variable to compute. Typically the wind speeds
    bins : list
        list of var category against we're going to compute the table
    nsector : integer
        number of sectors

    Other Parameters
    ----------------
    normed : boolean, default False
        The resulting table is normed in percent or not.
    blowto : boolean, default False
        Normally a windrose is computed with directions as wind blows from. If
        true, the table will be reversed (useful for pollutantrose)
    """

    if len(var) != len(direction):
        raise ValueError("var and direction must have same length")

    angle = 360.0 / nsector

    dir_bins = np.arange(
        -angle / 2 + sectoroffset,
        360.0 + angle + sectoroffset,
        angle,
        dtype=float,
    )
    dir_edges = dir_bins.tolist()
    dir_edges.pop(-1)
    dir_edges[0] = dir_edges.pop(-1)

    var_bins = bins.tolist()
    var_bins.append(np.inf)

    if blowto:
        direction = direction + 180.0
        direction[direction >= 360.0] = direction[direction >= 360.0] - 360

    table = histogram2d(x=var, y=direction, bins=[var_bins, dir_bins], density=False)[0]
    # add the last value to the first to have the table of North winds
    table[:, 0] = table[:, 0] + table[:, -1]
    # and remove the last col
    table = table[:, :-1]
    if normed:
        table = table * 100 / total

    return dir_edges, var_bins, table


@_copy_docstring(WindroseAxes.contour)
def wrcontour(direction, var, ax=None, rmax=None, figsize=FIGSIZE_DEFAULT, **kwargs):
    """
    Draw contour probability density function and return Weibull
    distribution parameters.
    """
    ax = WindroseAxes.from_ax(ax, rmax=rmax, figsize=figsize)
    ax.contour(direction, var, **kwargs)
    ax.set_legend()
    return ax


@_copy_docstring(WindroseAxes.contourf)
def wrcontourf(direction, var, ax=None, rmax=None, figsize=FIGSIZE_DEFAULT, **kwargs):
    ax = WindroseAxes.from_ax(ax, rmax=rmax, figsize=figsize)
    ax.contourf(direction, var, **kwargs)
    ax.set_legend()
    return ax


@_copy_docstring(WindroseAxes.box)
def wrbox(direction, var, ax=None, rmax=None, figsize=FIGSIZE_DEFAULT, **kwargs):
    ax = WindroseAxes.from_ax(ax, rmax=rmax, figsize=figsize)
    ax.box(direction, var, **kwargs)
    ax.set_legend()
    return ax


@_copy_docstring(WindroseAxes.bar)
def wrbar(direction, var, ax=None, rmax=None, figsize=FIGSIZE_DEFAULT, **kwargs):
    ax = WindroseAxes.from_ax(ax, rmax=rmax, figsize=figsize)
    ax.bar(direction, var, **kwargs)
    ax.set_legend()
    return ax


@_copy_docstring(WindAxes.pdf)
def wrpdf(
    var,
    bins=None,
    Nx=100,
    bar_color="b",
    plot_color="g",
    Nbins=10,
    ax=None,
    rmax=None,
    figsize=FIGSIZE_DEFAULT,
    *args,
    **kwargs,
):
    """
    Draw probability density function and return Weitbull distribution
    parameters
    """
    ax = WindAxes.from_ax(ax, figsize=figsize)
    ax, params = ax.pdf(var, bins, Nx, bar_color, plot_color, Nbins, *args, **kwargs)
    return (ax, params)


def wrscatter(
    direction,
    var,
    ax=None,
    rmax=None,
    figsize=FIGSIZE_DEFAULT,
    *args,
    **kwargs,
):
    """
    Draw scatter plot
    """
    ax = WindroseAxes.from_ax(ax, rmax=rmax, figsize=figsize)
    direction = -np.array(direction) + np.radians(90)
    ax.scatter(direction, var, *args, **kwargs)
    return ax


# def clean(direction, var):
#     '''
#     Remove masked values in the two arrays, where if a direction data is masked,
#     the var data will also be removed in the cleaning process (and vice-versa)
#     '''
#     dirmask = direction.mask==False
#     varmask = direction.mask==False
#     mask = dirmask*varmask
#     return direction[mask], var[mask]


def clean_df(df, var=VAR_DEFAULT, direction=DIR_DEFAULT):
    """
    Remove nan and var=0 values in the DataFrame
    if a var (wind speed) is nan or equal to 0, this row is
    removed from DataFrame
    if a direction is nan, this row is also removed from DataFrame
    """
    return df[df[var].notnull() & (df[var] != 0) & df[direction].notnull()]


def clean(direction, var, index=False):
    """
    Remove nan and var=0 values in the two arrays
    if a var (wind speed) is nan or equal to 0, this data is
    removed from var array but also from dir array
    if a direction is nan, data is also removed from both array
    """
    dirmask = np.isfinite(direction)
    varmask = (var != 0) & np.isfinite(var)
    mask = dirmask & varmask
    if index is None:
        index = np.arange(mask.sum())
        return direction[mask], var[mask], index
    elif not index:
        return direction[mask], var[mask]
    else:
        index = index[mask]
        return direction[mask], var[mask], index


D_KIND_PLOT = {
    "contour": wrcontour,
    "contourf": wrcontourf,
    "box": wrbox,
    "bar": wrbar,
    "pdf": wrpdf,
    "scatter": wrscatter,
}


def plot_windrose(
    direction_or_df,
    var=None,
    kind="contour",
    var_name=VAR_DEFAULT,
    direction_name=DIR_DEFAULT,
    by=None,
    rmax=None,
    ax=None,
    **kwargs,
):
    """Plot windrose from a pandas DataFrame or a numpy array."""
    if var is None:
        # Assuming direction_or_df is a DataFrame
        df = direction_or_df
        var = df[var_name].values
        direction = df[direction_name].values
    else:
        direction = direction_or_df
    return plot_windrose_np(
        direction,
        var,
        kind=kind,
        by=by,
        rmax=rmax,
        ax=ax,
        **kwargs,
    )


def plot_windrose_df(
    df,
    kind="contour",
    var_name=VAR_DEFAULT,
    direction_name=DIR_DEFAULT,
    by=None,
    rmax=None,
    ax=None,
    **kwargs,
):
    """Plot windrose from a pandas DataFrame."""
    var = df[var_name].values
    direction = df[direction_name].values
    return plot_windrose_np(
        direction,
        var,
        kind=kind,
        by=by,
        rmax=rmax,
        ax=ax,
        **kwargs,
    )


def plot_windrose_np(
    direction,
    var,
    kind="contour",
    clean_flag=True,
    by=None,
    rmax=None,
    ax=None,
    **kwargs,
):
    """Plot windrose from a numpy array."""
    if kind in D_KIND_PLOT.keys():
        f_plot = D_KIND_PLOT[kind]
    else:
        raise Exception(f"kind={kind!r} but it must be in {D_KIND_PLOT.keys()!r}")
    # if f_clean is not None:
    #     df = f_clean(df)
    # var = df[var_name].values
    # direction = df[direction_name].values
    if clean_flag:
        direction, var = clean(direction, var)
    if by is None:
        ax = f_plot(direction=direction, var=var, rmax=rmax, ax=ax, **kwargs)
        if kind not in ["pdf"]:
            ax.set_legend()
        return ax
    else:
        raise NotImplementedError(
            "'by' keyword not supported for now "
            "https://github.com/scls19fr/windrose/issues/10",
        )
