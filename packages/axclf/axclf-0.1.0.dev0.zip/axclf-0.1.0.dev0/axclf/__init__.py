"""
axclf

Save/restore Matplotlib axes limits during iterative and interactive
development.

This functionality becomes useful when using cell-mode functionality
in editors such as IdleX, Spyder, IEP, etc. During algorithm prototyping,
plots are generated. These helper routines allow for inspecting a
region of interest on a plot, and then running a change to see its effects
without needing to re-zoom/pan to the region of interest.

Author: Roger D. Serwy

"""

import matplotlib.pyplot as plt
from ._version import __version__


__all__ = ['axclf', 'axrestore', '__version__']


def axclf():
    """Save the active figure's axes limits and clear the figure"""
    f = plt.gcf()
    axes = f.get_axes()
    limits = []
    for n, a in enumerate(axes):
        x = a.get_xlim()
        y = a.get_ylim()
        limits.append((x,y))
    f.__axclf = limits
    f.clear()

def axrestore():
    """Restore the axes x and y limits"""
    f = plt.gcf()
    restore = getattr(f, '__axclf', None)
    if restore is None:
        return
    axes = f.get_axes()
    for ax, (x,y) in zip(axes, restore):
        ax.set_xlim(x)
        ax.set_ylim(y)
