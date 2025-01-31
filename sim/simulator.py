import datetime

import numpy as np
import pandas as pd
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)


class SimulatorSignal(QObject):
    threadFinished = Signal()
    updateSystemTime = Signal(str)
    updateTickPrice = Signal(str, float)
    updateTrend = Signal(int)


class WorkerSimulator(QRunnable, SimulatorSignal):
    def __init__(self, dict_target: dict):
        super().__init__()
        self.time_format = '%H:%M:%S'
        self.df_tick = dict_target['tick']
        self.df_ohlc_1m = dict_target['1m']
        self.date_str = dict_target['date_format']
        self.t_start = pd.to_datetime('%s 09:00:00' % self.date_str)
        self.t_end = pd.to_datetime('%s 15:31:00' % self.date_str)
        self.t_second = datetime.timedelta(seconds=1)
        self.t_minute = datetime.timedelta(minutes=1)

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

    def find_psar_trend(self, t_current):
        """
        PSAR トレンドを取得
        :param t_current:
        :return:
        """
        # t_current は 0 秒の時刻
        # １分足の OHLC が確定したのはその１分前の時刻のデータ
        # 同時に PSAR の算出も済んでいるものと仮定
        t_ohlc_latest = t_current - self.t_minute
        if t_ohlc_latest in self.df_ohlc_1m.index:
            trend = self.df_ohlc_1m.at[t_ohlc_latest, 'TREND']
            period = self.df_ohlc_1m.at[t_ohlc_latest, 'Period']
            diff = self.df_ohlc_1m.at[t_ohlc_latest, 'Diff']
            if not np.isnan(trend):
                self.updateTrend.emit(trend)

    def run(self):
        t_current = self.t_start

        while t_current <= self.t_end:
            # システム時刻の通知
            self.updateSystemTime.emit(
                t_current.strftime(self.time_format)
            )

            # ティックデータがあれば通知
            self.find_tick_data(t_current)

            # PSARトレンド
            if t_current.second == 0:
                self.find_psar_trend(t_current)

            # 時刻を１秒進める
            t_current += self.t_second

        # スレッド処理の終了を通知
        self.threadFinished.emit()
