import os
from datetime import timedelta

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from func.tide import get_range_xaxis
from structs.res import AppRes


def clearAxes(fig: Figure):
    """Clear axes

    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.cla()

def drawGrid(fig: Figure):
    """Draw grids

    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.grid()

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

        #self.ax = self.fig.add_subplot(111)
        self.ax = dict()
        n = 2
        gs = self.fig.add_gridspec(
            n, 1,
            wspace=0.0, hspace=0.0,
            height_ratios=[3 if i == 0 else 1 for i in range(n)]
        )
        for i, axis in enumerate(gs.subplots(sharex='col')):
            self.ax[i] = axis
            self.ax[i].grid()

        self.fig.subplots_adjust(
            left=0.05,
            right=0.99,
            top=0.98,
            bottom=0.06,
        )

    def plot(self, dict_df: dict):
        """
        プロット
        :param df:
        :return:
        """

        # 消去
        clearAxes(self.fig)

        df_tick = dict_df['tick']
        df_ohlc_1m = dict_df['1m']

        self.ax[0].plot(
            df_tick,
            color='black',
            linewidth='0.75',
            alpha=0.5,
        )

        df_bear = df_ohlc_1m[df_ohlc_1m['TREND'] < 0]
        df_bull = df_ohlc_1m[df_ohlc_1m['TREND'] > 0]

        # bear - Downward trend
        self.ax[0].scatter(
            x=df_bear.index,
            y=df_bear['PSAR'],
            color='blue',
            s=10,
        )

        # bull - Upward trend
        self.ax[0].scatter(
            x=df_bull.index,
            y=df_bull['PSAR'],
            color='red',
            s=10,
        )

        self.ax[0].set_ylabel('Price')

        self.ax[0].xaxis.set_major_formatter(
            mdates.DateFormatter('%H:%M')
        )
        self.ax[0].set_xlim(get_range_xaxis(df_tick))

        self.ax[1].set_yscale('log')
        self.ax[1].bar(
            df_ohlc_1m.index,
            df_ohlc_1m['Volume'],
            width=timedelta(minutes=1),
            align = 'center'
        )
        self.ax[1].set_ylabel('Volume')

        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
