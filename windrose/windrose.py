#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import absolute_import, division, print_function

import matplotlib as mpl
import numpy as np
from matplotlib.projections.polar import PolarAxes
from numpy.lib.twodim_base import histogram2d
import matplotlib.pyplot as plt
from pylab import poly_between

RESOLUTION = 100
ZBASE = -1000 #The starting zorder for all drawing, negative to have the grid on
VAR_DEFAULT = 'speed'
DIR_DEFAULT = 'direction'
FIGSIZE_DEFAULT = (8, 8)
DPI_DEFAULT = 80


class WindAxesFactory(object):
    # Create based on class name:
    @staticmethod
    def create(typ, ax=None, *args, **kwargs):
        typ = typ.lower()
        d = {
            'windroseaxes': WindroseAxes,
            'windaxes': WindAxes
        }
        if typ in d.keys():
            cls = d[typ]
            if isinstance(ax, cls):
                return ax
            else:
                ax = cls.from_ax(ax, *args, **kwargs)
                return ax
        else:
            raise(NotImplementedError("typ=%r but it might be in %s" % (typ, d.keys())))

class WindroseAxes(PolarAxes):
    """

    Create a windrose axes

    """

    def __init__(self, *args, **kwargs):
        """
        See Axes base class for args and kwargs documentation
        """
        
        #Uncomment to have the possibility to change the resolution directly 
        #when the instance is created
        #self.RESOLUTION = kwargs.pop('resolution', 100)
        PolarAxes.__init__(self, *args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.radii_angle = 67.5
        self.cla()

    @staticmethod
    def from_ax(ax=None, *args, **kwargs):
        if ax is None:
            fig = plt.figure(figsize=FIGSIZE_DEFAULT, dpi=DPI_DEFAULT, facecolor='w', edgecolor='w')
            rect = [0.1, 0.1, 0.8, 0.8]
            ax = WindroseAxes(fig, rect, axisbg='w', *args, **kwargs)
            fig.add_axes(ax)
            return ax
        else:
            return ax

    def cla(self):
        """
        Clear the current axes
        """
        PolarAxes.cla(self)

        self.theta_angles = np.arange(0, 360, 45)
        self.theta_labels = ['E', 'N-E', 'N', 'N-W', 'W', 'S-W', 'S', 'S-E']
        self.set_thetagrids(angles=self.theta_angles, labels=self.theta_labels)

        self._info = {'dir' : list(),
                      'bins' : list(),
                      'table' : list()}

        self.patches_list = list()


    def _colors(self, cmap, n):
        '''
        Returns a list of n colors based on the colormap cmap

        '''
        return [cmap(i) for i in np.linspace(0.0, 1.0, n)]


    def set_radii_angle(self, **kwargs):
        """
        Set the radii labels angle
        """

        kwargs.pop('labels', None)
        angle = kwargs.pop('angle', None)
        if angle is None:
            angle = self.radii_angle
        self.radii_angle = angle
        radii = np.linspace(0.1, self.get_rmax(), 6)
        radii_labels = [ "%.1f" %r for r in radii ]
        radii_labels[0] = "" #Removing label 0
        self.set_rgrids(radii=radii, labels=radii_labels,
                               angle=self.radii_angle, **kwargs)


    def _update(self):
        self.set_rmax(rmax=np.max(np.sum(self._info['table'], axis=0)))
        self.set_radii_angle(angle=self.radii_angle)


    def legend(self, loc='lower left', **kwargs):
        """
        Sets the legend location and her properties.
        The location codes are

          'best'         : 0,
          'upper right'  : 1,
          'upper left'   : 2,
          'lower left'   : 3,
          'lower right'  : 4,
          'right'        : 5,
          'center left'  : 6,
          'center right' : 7,
          'lower center' : 8,
          'upper center' : 9,
          'center'       : 10,

        If none of these are suitable, loc can be a 2-tuple giving x,y
        in axes coords, ie,

          loc = (0, 1) is left top
          loc = (0.5, 0.5) is center, center

        and so on.  The following kwargs are supported:

        isaxes=True           # whether this is an axes legend
        prop = FontProperties(size='smaller')  # the font property
        pad = 0.2             # the fractional whitespace inside the legend border
        shadow                # if True, draw a shadow behind legend
        labelsep = 0.005     # the vertical space between the legend entries
        handlelen = 0.05     # the length of the legend lines
        handletextsep = 0.02 # the space between the legend line and legend text
        borderaxespad = 0.02       # the border between the axes and legend edge
        """

        def get_handles():
            handles = list()
            for p in self.patches_list:
                if isinstance(p, mpl.patches.Polygon) or \
                isinstance(p, mpl.patches.Rectangle):
                    color = p.get_facecolor()
                elif isinstance(p, mpl.lines.Line2D):
                    color = p.get_color()
                else:
                    raise AttributeError("Can't handle patches")
                handles.append(mpl.patches.Rectangle((0, 0), 0.2, 0.2,
                    facecolor=color, edgecolor='black'))
            return handles

        def get_labels():
            labels = np.copy(self._info['bins'])
            labels = ["[%.1f : %0.1f[" %(labels[i], labels[i+1]) \
                      for i in range(len(labels)-1)]
            return labels

        kwargs.pop('labels', None)
        kwargs.pop('handles', None)
        handles = get_handles()
        labels = get_labels()
        self.legend_ = mpl.legend.Legend(self, handles, labels, loc, **kwargs)
        return self.legend_

    def set_legend(self):
        l = self.legend(borderaxespad=-0.10)
        plt.setp(l.get_texts(), fontsize=8)

    def _init_plot(self, direction, var, **kwargs):
        """
        Internal method used by all plotting commands
        """
        #self.cla()
        kwargs.pop('zorder', None)

        #Init of the bins array if not set
        bins = kwargs.pop('bins', None)
        if bins is None:
            bins = np.linspace(np.min(var), np.max(var), 6)
        if isinstance(bins, int):
            bins = np.linspace(np.min(var), np.max(var), bins)
        bins = np.asarray(bins)
        nbins = len(bins)

        #Number of sectors
        nsector = kwargs.pop('nsector', None)
        if nsector is None:
            nsector = 16

        #Sets the colors table based on the colormap or the "colors" argument
        colors = kwargs.pop('colors', None)
        cmap = kwargs.pop('cmap', None)
        if colors is not None:
            if isinstance(colors, str):
                colors = [colors]*nbins
            if isinstance(colors, (tuple, list)):
                if len(colors) != nbins:
                    raise ValueError("colors and bins must have same length")
        else:
            if cmap is None:
                cmap = mpl.cm.jet
            colors = self._colors(cmap, nbins)

        #Building the angles list
        angles = np.arange(0, -2*np.pi, -2*np.pi/nsector) + np.pi/2

        normed = kwargs.pop('normed', False)
        blowto = kwargs.pop('blowto', False)

        #Set the global information dictionnary
        self._info['dir'], self._info['bins'], self._info['table'] = histogram(direction, var, bins, nsector, normed, blowto)

        return bins, nbins, nsector, colors, angles, kwargs


    def contour(self, direction, var, **kwargs):
        """
        Plot a windrose in linear mode. For each var bins, a line will be
        draw on the axes, a segment between each sector (center to center).
        Each line can be formated (color, width, ...) like with standard plot
        pylab command.

        Mandatory:
        * direction : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6, then
            bins=linspace(min(var), max(var), 6)
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.

        others kwargs : see help(pylab.plot)

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(direction, var,
                                                                       **kwargs)

        #closing lines
        angles = np.hstack((angles, angles[-1]-2*np.pi/nsector))
        vals = np.hstack((self._info['table'],
                         np.reshape(self._info['table'][:,0],
                                   (self._info['table'].shape[0], 1))))
        
        offset = 0
        for i in range(nbins):
            val = vals[i,:] + offset
            offset += vals[i, :]
            zorder = ZBASE + nbins - i
            patch = self.plot(angles, val, color=colors[i], zorder=zorder,
                              **kwargs)
            self.patches_list.extend(patch)
        self._update()


    def contourf(self, direction, var, **kwargs):
        """
        Plot a windrose in filled mode. For each var bins, a line will be
        draw on the axes, a segment between each sector (center to center).
        Each line can be formated (color, width, ...) like with standard plot
        pylab command.

        Mandatory:
        * direction : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6, then
            bins=linspace(min(var), max(var), 6)
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.

        others kwargs : see help(pylab.plot)

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(direction, var,
                                                                       **kwargs)
        kwargs.pop('facecolor', None)
        kwargs.pop('edgecolor', None)
        
        #closing lines
        angles = np.hstack((angles, angles[-1]-2*np.pi/nsector))
        vals = np.hstack((self._info['table'],
                         np.reshape(self._info['table'][:,0],
                                   (self._info['table'].shape[0], 1))))
        offset = 0
        for i in range(nbins):
            val = vals[i,:] + offset
            offset += vals[i, :]
            zorder = ZBASE + nbins - i
            xs, ys = poly_between(angles, 0, val)
            patch = self.fill(xs, ys, facecolor=colors[i],
                              edgecolor=colors[i], zorder=zorder, **kwargs)
            self.patches_list.extend(patch)


    def bar(self, direction, var, **kwargs):
        """
        Plot a windrose in bar mode. For each var bins and for each sector,
        a colored bar will be draw on the axes.

        Mandatory:
        * direction : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6 between min(var) and max(var).
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.
        edgecolor : string - The string color each edge bar will be plotted.
        Default : no edgecolor
        * opening : float - between 0.0 and 1.0, to control the space between
        each sector (1.0 for no space)

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(direction, var,
                                                                       **kwargs)
        kwargs.pop('facecolor', None)
        edgecolor = kwargs.pop('edgecolor', None)
        if edgecolor is not None:
            if not isinstance(edgecolor, str):
                raise ValueError('edgecolor must be a string color')
        opening = kwargs.pop('opening', None)
        if opening is None:
            opening = 0.8
        dtheta = 2*np.pi/nsector
        opening = dtheta*opening

        for j in range(nsector):
            offset = 0
            for i in range(nbins):
                if i > 0:
                    offset += self._info['table'][i-1, j]
                val = self._info['table'][i, j]
                zorder = ZBASE + nbins - i
                patch = mpl.patches.Rectangle((angles[j]-opening/2, offset), opening, val,
                    facecolor=colors[i], edgecolor=edgecolor, zorder=zorder,
                    **kwargs)
                self.add_patch(patch)
                if j == 0:
                    self.patches_list.append(patch)
        self._update()


    def box(self, direction, var, **kwargs):
        """
        Plot a windrose in proportional bar mode. For each var bins and for each
        sector, a colored bar will be draw on the axes.

        Mandatory:
        * direction : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6 between min(var) and max(var).
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.
        edgecolor : string - The string color each edge bar will be plotted.
        Default : no edgecolor

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(direction, var,
                                                                       **kwargs)
        kwargs.pop('facecolor', None)
        edgecolor = kwargs.pop('edgecolor', None)
        if edgecolor is not None:
            if not isinstance(edgecolor, str):
                raise ValueError('edgecolor must be a string color')
        opening = np.linspace(0.0, np.pi/16, nbins)

        for j in range(nsector):
            offset = 0
            for i in range(nbins):
                if i > 0:
                    offset += self._info['table'][i-1, j]
                val = self._info['table'][i, j]
                zorder = ZBASE + nbins - i
                patch = mpl.patches.Rectangle((angles[j]-opening[i]/2, offset), opening[i],
                    val, facecolor=colors[i], edgecolor=edgecolor,
                    zorder=zorder, **kwargs)
                self.add_patch(patch)
                if j == 0:
                    self.patches_list.append(patch)
        self._update()


class WindAxes(mpl.axes.Subplot):
    def __init__(self, *args, **kwargs):
        """
        See Axes base class for args and kwargs documentation
        """
        super(WindAxes, self).__init__(*args, **kwargs)

    @staticmethod
    def from_ax(ax=None, *args, **kwargs):
        if ax is None:
            fig = plt.figure(figsize=FIGSIZE_DEFAULT, dpi=DPI_DEFAULT)
            ax = WindAxes(fig, 1, 1, 1, *args, **kwargs)
            fig.add_axes(ax)
            return ax
        else:
            return(ax)

    def pdf(self, var, bins=None, Nx=100, bar_color='b', plot_color='g', Nbins=10, *args, **kwargs):
        '''
        Draw probability density function
        and return Weibull distribution parameters
        '''
        import scipy.stats
        if bins is None:
            bins = np.linspace(0, np.max(var), Nbins)
        hist, bins = np.histogram(var, bins=bins, normed=True)
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        self.bar(center, hist, align='center', width=width, color=bar_color)
        params = scipy.stats.exponweib.fit(var, floc=0, f0=1)
        x = np.linspace(0, bins[-1], Nx)
        _ = self.plot(x, scipy.stats.exponweib.pdf(x, *params), color=plot_color)
        return(self, params)        


def histogram(direction, var, bins, nsector, normed=False, blowto=False):
    """
    Returns an array where, for each sector of wind
    (centred on the north), we have the number of time the wind comes with a
    particular var (speed, polluant concentration, ...).
    * direction : 1D array - directions the wind blows from, North centred
    * var : 1D array - values of the variable to compute. Typically the wind
        speeds
    * bins : list - list of var category against we're going to compute the table
    * nsector : integer - number of sectors
    * normed : boolean - The resulting table is normed in percent or not.
    * blowto : boolean - Normaly a windrose is computed with directions
    as wind blows from. If true, the table will be reversed (usefull for
    pollutantrose)

    """

    if len(var) != len(direction):
        raise(ValueError("var and direction must have same length"))

    angle = 360./nsector

    dir_bins = np.arange(-angle/2 ,360.+angle, angle, dtype=np.float)
    dir_edges = dir_bins.tolist()
    dir_edges.pop(-1)
    dir_edges[0] = dir_edges.pop(-1)
    dir_bins[0] = 0.

    var_bins = bins.tolist()
    var_bins.append(np.inf)

    if blowto:
        direction = direction + 180.
        direction[direction>=360.] = direction[direction>=360.] - 360

    table = histogram2d(x=var, y=direction, bins=[var_bins, dir_bins],
                          normed=False)[0]
    # add the last value to the first to have the table of North winds
    table[:,0] = table[:,0] + table[:,-1]
    # and remove the last col
    table = table[:, :-1]
    if normed:
        table = table*100/table.sum()

    return dir_edges, var_bins, table


def wrcontour(direction, var, ax=None, **kwargs):
    ax = WindroseAxes.from_ax(ax)
    ax.contour(direction, var, **kwargs)
    ax.set_legend()
    return ax


def wrcontourf(direction, var, ax=None, **kwargs):
    ax = WindroseAxes.from_ax(ax)
    ax.contourf(direction, var, **kwargs)
    ax.set_legend()
    return ax


def wrbox(direction, var, ax=None, **kwargs):
    ax = WindroseAxes.from_ax(ax)
    ax.box(direction, var, **kwargs)
    ax.set_legend()
    return ax


def wrbar(direction, var, ax=None, **kwargs):
    ax = WindroseAxes.from_ax(ax)
    ax.bar(direction, var, **kwargs)
    ax.set_legend()
    return ax


def wrpdf(var, bins=None, Nx=100, bar_color='b', plot_color='g', Nbins=10, ax=None, *args, **kwargs):
    '''
    Draw probability density function
    and return Weitbull distribution parameters
    '''
    ax = WindAxes.from_ax(ax)
    ax, params = ax.pdf(var, bins, Nx, bar_color, plot_color, *args, **kwargs)
    return(ax, params)


def wrscatter(direction, var, ax=None, *args, **kwargs):
    '''
    Draw scatter plot
    '''
    ax = WindroseAxes.from_ax(ax)
    ax.scatter(direction, var, *args, **kwargs)
    return ax


#def clean(direction, var):
#    '''
#    Remove masked values in the two arrays, where if a direction data is masked,
#    the var data will also be removed in the cleaning process (and vice-versa)
#    '''
#    dirmask = direction.mask==False
#    varmask = direction.mask==False
#    ind = dirmask*varmask
#    return direction[ind], var[ind]


def clean_df(df, var=VAR_DEFAULT, direction=DIR_DEFAULT):
    '''
    Remove nan and var=0 values in the DataFrame
    if a var (wind speed) is nan or equal to 0, this row is
    removed from DataFrame
    if a direction is nan, this row is also removed from DataFrame
    '''
    return(df[df[var].notnull() & df[var]!=0 & df[direction].notnull()])


def clean(direction, var):
    '''
    Remove nan and var=0 values in the two arrays
    if a var (wind speed) is nan or equal to 0, this data is
    removed from var array but also from dir array
    if a direction is nan, data is also removed from both array
    '''
    dirmask = np.isfinite(direction)
    varmask = (var!=0 & np.isfinite(var))
    ind = dirmask*varmask
    return direction[ind], var[ind]


D_KIND_PLOT = {
    'contour': wrcontour,
    'contourf': wrcontourf,
    'box': wrbox,
    'bar': wrbar,
    'pdf': wrpdf,
    'scatter': wrscatter
}


def plot_windrose(df, kind='contour', var_name=VAR_DEFAULT, direction_name=DIR_DEFAULT, f_clean=clean_df, **kwargs):
    if kind in D_KIND_PLOT.keys():
        f_plot = D_KIND_PLOT[kind]
    else:
        raise(Exception("kind=%r but it must be in %r" % (kind, d.keys())))
    if f_clean is not None:
        df = f_clean(df)
    var = df[var_name].values
    direction = df[direction_name].values
    ax = f_plot(direction=direction, var=var, **kwargs)
    if kind not in ['pdf']:
        ax.set_legend()
    return ax
