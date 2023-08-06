# Copyright Ryan Hausen 2019
# The MIT License (MIT)
#
# Copyright (c) 2019
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
from typing import List, Tuple

import cmocean
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar


class FigureHelper:
    """Handles the scope and some style in the figure."""

    cmap = cmocean.cm.dense_r
    marg_hist_color = "#7960c7"

    def __init__(self, fig_kwargs, add_legend=False, path=None):
        self.fig_kwargs = fig_kwargs
        font_loc = os.path.join(os.path.dirname(__file__), "fonts/Roboto-Regular.ttf")
        self.prop = fm.FontProperties(fname=font_loc)
        self.add_legend = add_legend
        self.path = path

    def __enter__(self):
        self.figure = plt.figure(**self.fig_kwargs)
        return self

    def __exit__(self, type, value, traceback):
        axes = self.figure.get_axes()

        for ax in axes:
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontproperties(self.prop)

            ax.set_xlabel(ax.get_xlabel(), font_properties=self.prop)
            ax.set_ylabel(ax.get_ylabel(), font_properties=self.prop)

        if self.add_legend:
            plt.legend(prop=self.prop)

        if self.path:
            plt.savefig(path=self.path, dpi=600, bbox_inches="tight")

    @staticmethod
    def get_color_list(n):
        return FigureHelper.cmap(np.linspace(0, 1, n + 1))[:-1]

    @staticmethod
    def negative_helper(x, pos):
        x = str(x)
        pad = "" if x.startswith("-") else " "
        return "{}{}".format(pad, x)


def line_plot(
    x: np.ndarray,
    ys: List[np.ndarray],
    labels: List[str],
    x_label: str = "X",
    y_label: str = "Y",
    figsize: Tuple[int, int] = None,
    out_dir: str = None,
):
    """Makes a line plot."""

    fig_kwargs = {"figsize": figsize, "tight_layout": True}

    with FigureHelper(fig_kwargs, path=out_dir) as fig_helper:
        fig = fig_helper.figure
        ax = fig.add_subplot(111)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        colors = FigureHelper.get_color_list(len(ys))
        for y, c, l in zip(ys, colors, labels):
            ax.plot(x, y, color=c, label=l)


def imshow(
    arr: np.ndarray,
    x_label: str = "X",
    y_label: str = "Y",
    out_dir: str = None,
    cmap: str = None,
    origin: str = "lower",
    cbar_loc: str = "right",
    cbar_orientation: str = "vertical",
    cbar_label: str = "N",
    vmin: float = None,
    vmax: float = None,
    figsize: Tuple[int, int] = None,
    log: bool = False,
    scale_bar_size_lbl_loc: Tuple[float, int, int] = None,
):
    """Graphs a single array with colorbars and labels."""

    fig_kwargs = {"figsize": figsize, "tight_layout": True}

    with FigureHelper(fig_kwargs, path=out_dir) as fig_helper:
        fig = fig_helper.figure
        color_norm = LogNorm() if log else Normalize()

        # image
        ax = fig.add_subplot(111)

        im = ax.imshow(
            arr,
            cmap=cmap if cmap else FigureHelper.cmap,
            origin=origin,
            interpolation="none",
            vmin=vmin,
            vmax=vmax,
            norm=color_norm,
        )

        print(fig.__dict__)

        if scale_bar_size_lbl_loc:
            size_bar = AnchoredSizeBar(
                ax.transData,
                scale_bar_size_lbl_loc[0],
                scale_bar_size_lbl_loc[1],
                scale_bar_size_lbl_loc[2],
                fontproperties=fig_helper.prop,
            )

            ax.add_artist(size_bar)
            ax.axis("off")
        else:
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)

        # color bar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes(cbar_loc, size="2%", pad=0.05)
        cb = fig.colorbar(im, cax=cax, orientation=cbar_orientation)

        fmt = mpl.ticker.FuncFormatter(FigureHelper.negative_helper)
        if cbar_orientation == "vertical":
            cb.ax.yaxis.major.formatter = fmt
            cb.ax.set_ylabel(cbar_label)
        if cbar_orientation == "horizontal":
            cb.ax.xaxis.major.formatter = fmt
            cb.ax.set_xlabel(cbar_label)


def historgram2d(
    x1: np.ndarray,
    x2: np.ndarray,
    out_dir: str = None,
    cmap: str = None,
    xbins: int = 100,
    ybins: int = 100,
    x_label: str = "X",
    y_label: str = "Y",
    joint_color_log: bool = False,
    marg_x_log: bool = False,
    marg_y_log: bool = False,
    figsize: Tuple[int, int] = None,
    flip_joint_x: bool = False,
    flip_joint_y: bool = False,
):
    """Makes a 2d histogram."""

    fig_kwargs = {"figsize": figsize, "tight_layout": True}

    with FigureHelper(fig_kwargs, path=out_dir) as fig_helper:
        fig = fig_helper.figure
        grid = GridSpec(4, 4)

        # joint histogram ======================================================
        ax_joint = fig.add_subplot(grid[1:4, 0:3])
        ax_joint.set_xlabel(x_label)
        ax_joint.set_ylabel(y_label)

        color_norm = LogNorm() if joint_color_log else Normalize()

        joint_hist = ax_joint.hist2d(
            x1, x2, bins=(xbins, ybins), norm=color_norm, cmap=FigureHelper.cmap
        )

        divider = make_axes_locatable(ax_joint)
        cax = divider.append_axes("right", size="2%", pad=0.05)
        cb = fig.colorbar(joint_hist[-1], cax=cax, orientation="vertical")

        # ======================================================================

        # marginal x histogram =================================================
        ax_marg_x = fig.add_subplot(grid[0, 0:3], sharex=ax_joint)
        ax_marg_x.set_ylabel("N")
        n, bins, patches = ax_marg_x.hist(
            x1, bins=xbins, color=FigureHelper.marg_hist_color, log=marg_x_log
        )

        if flip_joint_x:
            ax_marg_x.set_xlim([x1.max(), x1.min()])
        else:
            ax_marg_x.set_xlim([x1.min(), x1.max()])
        # ======================================================================

        # marginal y histogram =================================================
        ax_marg_y = fig.add_subplot(grid[1:4, 3], sharey=ax_joint)
        ax_marg_y.set_xlabel("N")
        n, bins, patches = ax_marg_y.hist(
            x2,
            orientation="horizontal",
            bins=ybins,
            color=FigureHelper.marg_hist_color,
            log=marg_y_log,
        )

        if flip_joint_y:
            ax_marg_y.set_ylim([x2.max(), x2.min()])
        else:
            ax_marg_y.set_ylim([x2.min(), x2.max()])
        # ======================================================================
