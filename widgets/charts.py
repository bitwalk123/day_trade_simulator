import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

from funcs.plots import (
    clearAxes,
    drawGrid,
    getMajorXTicks,
    refreshDraw,
)
from funcs.tide import get_range_xaxis
from structs.pair import PairXY
from structs.res import AppRes


class Canvas(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        font = os.path.join(
            res.dir_font,
            'RictyDiminished-Regular.ttf',
        )
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = dict()
        n = 4

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
            left=0.09,
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
            linewidth=0.5,
            alpha=0.5,
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

        # X軸の時刻刻みを調整
        tick_position, tick_labels = getMajorXTicks(df_tick)
        self.ax[0].set_xticks(
            ticks=tick_position,
            labels=tick_labels,
        )
        self.ax[0].xaxis.set_major_formatter(
            mdates.DateFormatter('%H:%M')
        )
        """
        self.ax[0].xaxis.set_minor_locator(
            mdates.MinuteLocator(interval=5)
        )
        """
        self.ax[0].set_xlim(
            get_range_xaxis(df_tick)
        )

        # Diff
        df_diff = df_ohlc_1m['Diff']
        self.ax[1].plot(
            df_diff,
            linewidth=0.75,
            color='black',
            alpha=0.75,
        )
        self.ax[1].set_ylabel('Profit/Loss')

        # ax[1] では　y = 0 を黒線で表示、正負を解りやすくする。
        self.ax[1].axhline(
            0,
            linewidth=0.75,
            color='#444',
        )

        # Slope
        df_slope = df_ohlc_1m['Slope']
        self.ax[2].plot(
            df_slope,
            linewidth=0.75,
            color='black',
            alpha=0.75,
        )
        self.ax[2].axhline(
            0,
            linewidth=0.75,
            color='#444',
        )
        self.ax[2].set_ylabel('Slope')

        # IQR
        df_iqr = df_ohlc_1m['IQR']
        self.ax[3].plot(
            df_iqr,
            linewidth=0.75,
            color='black',
            alpha=0.75,
        )
        self.ax[3].axhline(
            0,
            linewidth=0.75,
            color='#444',
        )
        self.ax[3].set_ylabel('IQR')

        # 売買タイミング
        df_transaction = dict_target['transaction']
        # １つ飛びでループ
        num = int(len(df_transaction) / 2)
        for idx in range(num):
            r1 = idx * 2
            r2 = r1 + 1
            dt1 = df_transaction.index[r1]
            dt2 = df_transaction.index[r2]
            if df_transaction.iat[r1, 0] == '売建':
                color = 'blue'
            elif df_transaction.iat[r1, 0] == '買建':
                color = 'red'
            else:
                color = 'black'

            for i in self.ax.keys():
                self.ax[i].fill_between(
                    [dt1, dt2], 0.05, 0.95,
                    color=color,
                    alpha=0.1,
                    transform=self.ax[i].get_xaxis_transform(),
                )

                self.ax[i].axvline(
                    dt1,
                    linewidth=0.5,
                    color=color,
                    alpha=0.25,
                )

                self.ax[i].axvline(
                    dt2,
                    linewidth=0.5,
                    color=color,
                    alpha=0.25,
                )

        # グリッド線
        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)


class ChartOverlay(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        font = os.path.join(
            res.dir_font,
            'RictyDiminished-Regular.ttf',
        )
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = self.fig.add_subplot(111)

        self.fig.subplots_adjust(
            left=0.1,
            right=0.95,
            top=0.99,
            bottom=0.05,
        )

        self.x_max = None
        self.y_min = None
        self.y_max = None

    def plot(self, list_obj: list):
        # 消去
        clearAxes(self.fig)

        for obj in list_obj:
            self.plotEach(obj)
        self.ax.axhline(
            0,
            linewidth=0.75,
            color='#444',
        )
        self.ax.set_xlim(0, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        # グリッド線
        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)

    def plotSingle(self, obj: PairXY):
        # 消去
        clearAxes(self.fig)

        self.ax.plot(
            obj.getX(), obj.getY(),
        )
        self.ax.axhline(
            0,
            linewidth=0.75,
            color='#444',
        )
        self.ax.set_xlim(0, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        # グリッド線
        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)

    def plotEach(self, obj: PairXY):
        self.ax.plot(
            obj.getX(), obj.getY(),
        )

    def plotBlank(self):
        # 消去
        clearAxes(self.fig)

        self.ax.axhline(
            0,
            linewidth=0.75,
            color='#444',
        )
        self.ax.set_xlim(0, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        # グリッド線
        drawGrid(self.fig)

    def plotReflesh(self):
        # 再描画
        refreshDraw(self.fig)

    def setAxisRange(self, x_max, y_min, y_max):
        self.x_max = x_max
        y_pad = (y_max - y_min) * 0.05
        self.y_min = y_min - y_pad
        self.y_max = y_max + y_pad


class Contour(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        font = os.path.join(
            res.dir_font,
            'RictyDiminished-Regular.ttf',
        )
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = self.fig.add_subplot(111)

        self.fig.subplots_adjust(
            left=0.1,
            right=0.975,
            top=0.975,
            bottom=0.1,
        )

    def plot(self, dict_data: dict):
        # 消去
        clearAxes(self.fig)

        x = dict_data['x']
        y = dict_data['y']
        z = dict_data['z']
        cont = self.ax.contour(
            x, y, z,
            colors=['blue'],
            linestyles='solid',
            linewidths=0.5,
        )
        cont.clabel(
            fmt='%.f',
            fontsize=12,
        )

        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        self.ax.set_xlabel(dict_data['param_x'], fontsize=16)
        self.ax.set_ylabel(dict_data['param_y'], fontsize=16)

        # グリッド線
        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
