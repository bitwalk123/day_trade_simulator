import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import mplfinance as mpf
import pandas as pd

from structs.res import AppRes


def clear_axes(fig: Figure):
    """Clear axes

    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.cla()


def refreshDraw(fig: Figure):
    fig.canvas.draw()


class Canvas(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        font = os.path.join(res.dir_font, 'RictyDiminished-Regular.ttf')
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(
            left=0.05,
            right=0.99,
            top=0.98,
            bottom=0.06,
        )

    def plot(self, df: pd.DataFrame):
        """
        プロット
        :param df:
        :return:
        """

        # 消去
        clear_axes(self.fig)

        self.plot_candle(df)

        # 再描画
        refreshDraw(self.fig)

    def plot_candle(self, df):
        """
        ローソク足チャート
        :param df:
        :return:
        """
        apds = [
            mpf.make_addplot(
                df['bear'],
                type='scatter',
                marker='o',
                markersize=5,
                color='blue',
                label='Down trend',
                ax=self.ax
            ),
            mpf.make_addplot(
                df['bull'],
                type='scatter',
                marker='o',
                markersize=5,
                color='red',
                label='Up trend',
                ax=self.ax
            ),
        ]
        mpf.plot(
            data=df,
            type='candle',
            style='default',
            datetime_format='%H:%M',
            xrotation=0,
            addplot=apds,
            ax=self.ax,
        )
        self.ax.grid()
        self.ax.legend(loc='best', fontsize=9)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
