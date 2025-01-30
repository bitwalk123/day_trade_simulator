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

        self.ax = dict()
        n = 2

        if n > 1:
            gs = self.fig.add_gridspec(
                n, 1,
                wspace=0.0, hspace=0.0,
                height_ratios=[2 if i == 0 else 1 for i in range(n)]
            )
            for i, axis in enumerate(gs.subplots(sharex='col')):
                self.ax[i] = axis
        else:
            self.ax[0] = self.fig.add_subplot(111)

        self.fig.subplots_adjust(
            left=0.08,
            right=0.99,
            top=0.95,
            bottom=0.06,
        )

    def plot(self, dict_target: dict):
        """
        プロット
        :param dict_target:
        :return:
        """

        # 消去
        clearAxes(self.fig)

        # ティックデータ
        df_tick = dict_target['tick']
        df_ohlc_1m = dict_target['1m']

        # Tick
        self.ax[0].plot(
            df_tick,
            color='black',
            linewidth='0.75',
            alpha=0.25,
        )

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

        # チャート・タイトル
        title_chart = '%s (%s) on %s' % (
            dict_target['name'],
            dict_target['code'],
            dict_target['date_format'],
        )
        self.ax[0].set_title(title_chart)

        # Y軸タイトル
        self.ax[0].set_ylabel('Price')

        tick_position, tick_labels = getMajorXTicks(df_tick)
        self.ax[0].set_xticks(ticks=tick_position, labels=tick_labels)
        self.ax[0].xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))
        self.ax[0].xaxis.set_major_formatter(
            mdates.DateFormatter('%H:%M')
        )
        self.ax[0].set_xlim(get_range_xaxis(df_tick))

        # Diff
        df_diff = df_ohlc_1m['Diff']
        self.ax[1].plot(
            df_diff,
            linewidth=0.75,
            color='black',
        )
        self.ax[1].set_ylabel('Diff')

        #d = timedelta(minutes=1)
        df_period = df_ohlc_1m[df_ohlc_1m['Period'] == 1]
        # print(df_period)
        for t in df_period.index:
            self.ax[0].axvline(t, linewidth=1, color='magenta', linestyle='dotted')
            self.ax[1].axvline(t, linewidth=1, color='magenta', linestyle='dotted')

        self.ax[1].axhline(0, linewidth=0.75, color='#444')

        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
