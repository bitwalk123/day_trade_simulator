import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from matplotlib import dates as mdates
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

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

        font = os.path.join(res.dir_font, 'RictyDiminished-Regular.ttf')
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
                height_ratios=[3 if i == 0 else 1 for i in range(n)]
            )
            for i, axis in enumerate(gs.subplots(sharex='col')):
                self.ax[i] = axis
        else:
            self.ax[0] = self.fig.add_subplot(111)

        self.fig.subplots_adjust(left=0.07, right=0.99, top=0.92, bottom=0.06)

    def plot(self, dict_plot: dict):
        """
        プロット
        :param dict_plot:
        :return:
        """

        # 消去
        clearAxes(self.fig)

        # ティックデータ
        df_tick = dict_plot['tick']

        # 含み益データ
        df_profit = dict_plot['profit']

        # =============
        #  ティックデータ
        # =============
        idx = 0
        self.ax[idx].plot(df_tick['Price'], color='black', linewidth=0.5, alpha=0.25)
        self.ax[idx].plot(df_tick['MMPrice'], color='black', linewidth=0.5, alpha=1)

        # PSAR トレンド
        df_bear = df_tick[df_tick['TREND'] < 0]
        df_bull = df_tick[df_tick['TREND'] > 0]
        for df, color in zip([df_bear, df_bull], ['blue', 'red']):
            self.ax[idx].scatter(x=df.index, y=df['PSAR'], color=color, s=5)

        # EP トレンド
        self.ax[idx].plot(df_tick['EP'], linewidth=1.25, linestyle='dotted', color='magenta', alpha=1, label=r'$EP$')

        # ロスカット用補助線
        if 'Losscut' in df_tick.columns:
            self.ax[0].plot(df_tick['Losscut'], linewidth=1, linestyle='dashed', color='#040', label='Losscut')

        # 含み損益を色分けして塗りつぶす
        if 'Baseline' in df_tick.columns:
            # Price vs. Baseline
            color_gain = '#00c'
            color_loss = '#c00'
            alpha = 0.1

            x = df_bear.index
            y1 = df_bear['Price']
            y2 = df_bear['Baseline']
            self.ax[idx].fill_between(x, y1, y2, where=(y1 < y2), color=color_gain, alpha=alpha)
            self.ax[idx].fill_between(x, y1, y2, where=(y1 > y2), color=color_loss, alpha=alpha)

            x = df_bull.index
            y1 = df_bull['Price']
            y2 = df_bull['Baseline']
            self.ax[idx].fill_between(x, y1, y2, where=(y1 > y2), color=color_gain, alpha=alpha)
            self.ax[idx].fill_between(x, y1, y2, where=(y1 < y2), color=color_loss, alpha=alpha)

        # チャート・タイトル
        self.fig.suptitle(dict_plot['title'])
        self.ax[idx].set_title(dict_plot['subtitle'], fontsize='small')

        # Y1軸タイトル
        self.ax[idx].set_ylabel(dict_plot['ylabel_tick'])

        # X軸の時刻刻みを調整
        tick_position, tick_labels = getMajorXTicks(df_tick)
        self.ax[idx].set_xticks(ticks=tick_position, labels=tick_labels)
        self.ax[idx].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax[idx].set_xlim(get_range_xaxis(df_tick))

        # 判例
        self.ax[idx].legend(fontsize=9)

        # 含み益トレンド
        if len(df_profit) > 0:
            idx += 1
            self.ax[idx].set_ylabel(dict_plot['ylabel_profit'])
            self.plot_profit(idx, df_profit)

        # Trend 継続回数
        colname = 'TrendN'
        if colname in df_tick.columns:
            idx += 1
            self.plot_trendn(idx, df_tick, colname)

        # EP 更新回数
        colname = 'EPupd'
        if colname in df_tick.columns:
            idx += 1
            self.plot_epupd(idx, df_tick, colname)

        # グリッド線
        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)

    def plot_epupd(self, idx, df_tick, colname):
        self.ax[idx].set_ylabel('EP updated')
        self.ax[idx].plot(df_tick[colname])
        _, y_max = self.ax[idx].get_ylim()
        if y_max > 50:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 10))
        else:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 5))

        self.ax[idx].tick_params(axis='y', labelsize=9)
        # y = 0 の横線
        self.ax[idx].axhline(0, linewidth=0.75, color='#444')

    def plot_profit(self, idx: int, df_profit: pd.DataFrame):
        self.ax[idx].plot(df_profit['Profit'], color='black', linewidth=0.5, alpha=0.75)
        self.ax[idx].plot(df_profit['ProfitMax'], color='red', linewidth=0.5, alpha=0.75)
        self.ax[idx].tick_params(axis='y', labelsize=9)
        # y = 0 の横線
        self.ax[idx].axhline(0, linewidth=0.75, color='#444')

    def plot_trendn(self, idx, df_tick, colname):
        self.ax[idx].set_ylabel('TrendN')
        self.ax[idx].plot(df_tick[colname])
        _, y_max = self.ax[idx].get_ylim()
        if y_max > 10000:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 2000))
        elif y_max > 5000:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 1000))
        elif y_max > 1000:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 500))
        elif y_max > 500:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 100))
        elif y_max > 100:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 20))
        else:
            self.ax[idx].yaxis.set_ticks(np.arange(0, y_max, 10))

        self.ax[idx].tick_params(axis='y', labelsize=9)
        # y = 0 の横線
        self.ax[idx].axhline(0, linewidth=0.75, color='#444')

    def save(self, filename):
        self.fig.savefig(filename)


class ChartOverlay(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        font = os.path.join(res.dir_font, 'RictyDiminished-Regular.ttf')
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = self.fig.add_subplot(111)

        self.fig.subplots_adjust(left=0.1, right=0.95, top=0.99, bottom=0.05)

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

        self.ax.plot(obj.getX(), obj.getY())
        self.ax.axhline(0, linewidth=0.75, color='#444')
        self.ax.set_xlim(0, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        # グリッド線
        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)

    def plotEach(self, obj: PairXY):
        self.ax.plot(obj.getX(), obj.getY())

    def plotBlank(self):
        # 消去
        clearAxes(self.fig)

        self.ax.axhline(0, linewidth=0.75, color='#444')
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

        font = os.path.join(res.dir_font, 'RictyDiminished-Regular.ttf')
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = self.fig.add_subplot(111)

        self.fig.subplots_adjust(left=0.1, right=0.975, top=0.975, bottom=0.1)

    def plot(self, dict_data: dict):
        # 消去
        clearAxes(self.fig)

        x = dict_data['x']
        y = dict_data['y']
        z = dict_data['z']
        cont = self.ax.contour(x, y, z, colors=['blue'], linestyles='solid', linewidths=0.5)
        cont.clabel(fmt='%.f', fontsize=12)

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
