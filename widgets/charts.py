import os
import pandas as pd
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
        ax.grid(which='major', linestyle='solid')
        ax.grid(which='minor', linestyle='dotted')


def refreshDraw(fig: Figure):
    fig.canvas.draw()


def getMajorXTicks(df: pd.DataFrame) -> tuple:
    date_str = str(df.index[0].date())
    tick_labels = [
        '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00',
        '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
    ]
    tick_position = [pd.to_datetime('%s %s' % (date_str, l)) for l in tick_labels]
    return tick_position, tick_labels


class Canvas(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        font = os.path.join(res.dir_font, 'RictyDiminished-Regular.ttf')
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        # self.ax = self.fig.add_subplot(111)
        self.ax = dict()
        n = 2
        gs = self.fig.add_gridspec(
            n, 1,
            wspace=0.0, hspace=0.0,
            height_ratios=[2 if i == 0 else 1 for i in range(n)]
        )
        for i, axis in enumerate(gs.subplots(sharex='col')):
            self.ax[i] = axis

        self.fig.subplots_adjust(
            left=0.075,
            right=0.99,
            top=0.98,
            bottom=0.06,
        )

    def plot(self, dict_df: dict):
        """
        プロット
        :param dict_df:
        :return:
        """

        # 消去
        clearAxes(self.fig)

        df_tick = dict_df['tick']
        # df_ohlc_1m = dict_df['1m']
        # print(df_ohlc_1m)

        # Tick
        self.ax[0].plot(
            df_tick,
            color='black',
            linewidth='0.75',
            alpha=0.5,
        )

        """
        df_bear = df_ohlc_1m[df_ohlc_1m['TREND'] < 0]
        df_bull = df_ohlc_1m[df_ohlc_1m['TREND'] > 0]

        # PSAR bear - Downward trend
        self.ax[0].scatter(
            x=df_bear.index,
            y=df_bear['PSAR'],
            color='blue',
            s=10,
        )

        # PSAR bull - Upward trend
        self.ax[0].scatter(
            x=df_bull.index,
            y=df_bull['PSAR'],
            color='red',
            s=10,
        )
        """

        self.ax[0].set_ylabel('Price')

        tick_position, tick_labels = getMajorXTicks(df_tick)
        self.ax[0].set_xticks(ticks=tick_position, labels=tick_labels)
        self.ax[0].xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))
        self.ax[0].xaxis.set_major_formatter(
            mdates.DateFormatter('%H:%M')
        )
        self.ax[0].set_xlim(get_range_xaxis(df_tick))

        # OBV, On-Valance Volume
        """
        self.ax[1].plot(
            df_ohlc_1m['OBV'],
            color='magenta',
        )
        self.ax[1].set_ylabel('On-Balance Volume')
        """

        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
