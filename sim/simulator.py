import datetime

import numpy as np
import pandas as pd
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)

from sim.trader import Trader


class SimulatorSignal(QObject):
    threadFinished = Signal()
    updateProfit = Signal(dict)
    updateSystemTime = Signal(str)
    updateTickPrice = Signal(str, float)
    updateTime = Signal(int)
    updateTrend = Signal(int)


class WorkerSimulator(QRunnable, SimulatorSignal):
    def __init__(self, dict_target: dict):
        super().__init__()
        self.time_format = '%H:%M:%S'
        self.df_tick = dict_target['tick']
        self.df_ohlc_1m = dict_target['1m']
        self.date_str = dict_target['date_format']
        self.t_start = pd.to_datetime('%s 09:00:00' % self.date_str)
        self.t_end_1h = pd.to_datetime('%s 11:29:50' % self.date_str)
        self.t_start_2h = pd.to_datetime('%s 12:30:00' % self.date_str)
        self.t_end_2h = pd.to_datetime('%s 15:24:50' % self.date_str)
        self.t_end = pd.to_datetime('%s 15:31:00' % self.date_str)

        self.t_second = datetime.timedelta(seconds=1)
        self.t_minute = datetime.timedelta(minutes=1)

        self.trader = Trader(dict_target['unit'])

    def getTimeRange(self):
        return self.t_start.timestamp(), self.t_end.timestamp()


    def run(self):
        t_current = self.t_start
        p_current = 0

        trend = 0
        period = 0
        diff = 0

        while t_current <= self.t_end:
            # システム時刻の通知
            self.updateSystemTime.emit(
                t_current.strftime(self.time_format)
            )

            # ティックデータがあれば通知
            tick_price = self.find_tick_data(t_current)
            if not np.isnan(tick_price):
                p_current = tick_price

            # PSARトレンド
            if t_current.second == 0:
                trend = self.trader.getTrend()
                trend, period, diff = self.find_psar_trend(t_current)
                # print(t_current, trend, period, diff)

            profit = self.trader.getProfit(p_current)
            profit_max = self.trader.getProfitMax()

            if t_current <= self.t_end_1h or (self.t_start_2h <= t_current <= self.t_end_2h):
                # PSAR トレンド判定
                if self.trader.getTrend() != trend:
                    self.trader.setTrend(trend)
                    # 建玉返済
                    self.sessionClosePos(t_current, p_current)
                    # 反対売買
                    self.sessionOpenPos(t_current, p_current)
            else:
                # 建玉返済
                self.sessionClosePos(t_current, p_current, '強制')

            # 収益の更新
            dict_update = {
                '建玉価格': self.trader.getPrice(),
                '売買': self.trader.getPosition(),
                '含み損益': profit,
                '最大含み益': profit_max,
                '合計損益': self.trader.getTotal(),
            }
            self.updateProfit.emit(dict_update)

            self.updateTime.emit(t_current.timestamp())
            # 時刻を１秒進める
            t_current += self.t_second

        # スレッド処理の終了を通知
        self.threadFinished.emit()

    def find_tick_data(self, t_current):
        """
        現在時刻のティックデータがあれば通知
        :param t_current:
        :return:
        """
        if t_current in self.df_tick.index:
            p_current = self.df_tick.at[t_current, 'Price']

            # 現在値詳細時刻と現在値を通知
            self.updateTickPrice.emit(
                t_current.strftime(self.time_format),
                p_current
            )
            return p_current
        else:
            return np.nan

    def find_psar_trend(self, t_current):
        """
        PSAR トレンドを取得
        :param t_current:
        :return:
        """
        trend = np.nan
        period = np.nan
        diff = np.nan

        # t_current は 0 秒の時刻
        # １分足の OHLC が確定したのはその１分前の時刻のデータ
        # 同時に PSAR の算出も済んでいるものと仮定
        t_ohlc_latest = t_current - self.t_minute
        if t_ohlc_latest in self.df_ohlc_1m.index:
            trend = self.df_ohlc_1m.at[t_ohlc_latest, 'TREND']
            period = self.df_ohlc_1m.at[t_ohlc_latest, 'Period']
            diff = self.df_ohlc_1m.at[t_ohlc_latest, 'Diff']
            if not np.isnan(trend):
                # 取得したトレンドを通知
                self.updateTrend.emit(trend)

        return trend, period, diff

    def sessionOpenPos(self, t, p, note=''):
        if not self.trader.hasPosition():
            transaction = dict()
            self.trader.openPosition(t, p, transaction, note)

    def sessionClosePos(self, t, p, note=''):
        if self.trader.hasPosition():
            transaction = dict()
            self.trader.closePosition(t, p, transaction, note)
