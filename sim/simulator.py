import datetime

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


class WorkerSimulator(QRunnable, SimulatorSignal):
    def __init__(self, dict_target: dict):
        super().__init__()
        self.timm_format = '%H:%M:%S'
        self.df_tick = dict_target['tick']
        self.df_ohlc_1m = dict_target['1m']
        self.date_str = dict_target['date_format']
        self.t_start = pd.to_datetime('%s 09:00:00' % self.date_str)
        self.t_end = pd.to_datetime('%s 15:31:00' % self.date_str)

    def run(self):
        t_current = self.t_start
        t_delta = datetime.timedelta(seconds=1)

        while t_current <= self.t_end:
            # システム時刻の通知
            self.updateSystemTime.emit(
                t_current.strftime(self.timm_format)
            )

            # ティックデータがあれば通知
            self.find_tick_data(t_current)

            t_current += t_delta

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
                t_current.strftime(self.timm_format),
                p_current
            )
