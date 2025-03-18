import datetime

import pandas as pd
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)


class SimulatorSignal(QObject):
    threadFinished = Signal(pd.DataFrame)
    updateSystemTime = Signal(str, int)
    updateTickPrice = Signal(str, float)


class WorkerSimulator(QRunnable, SimulatorSignal):
    def __init__(self, dict_info: dict):
        super().__init__()
        self.dict_info = dict_info
        self.ser_tick: pd.Series = self.dict_info['tick']

        # 時刻フォーマット用文字列
        self.time_format = '%H:%M:%S'

        # 取引時間
        self.t_start = pd.to_datetime('%s 09:00:00' % dict_info['date'])
        self.t_end = pd.to_datetime('%s 15:30:00' % dict_info['date'])

        # シミュレータ用時間定数
        self.t_second = datetime.timedelta(seconds=1)  # 1 秒

        # プロット用データフレーム
        dict_columns = {
            'Price': [],
            'TREND': [],
            'EP': [],
            'AF': [],
            'PSAR': [],
        }
        df = pd.DataFrame.from_dict(dict_columns)
        df.index.name = 'Datetime'
        self.df = df.astype(float)

    def get_progress(self, t) -> int:
        numerator = (t.timestamp() - self.t_start.timestamp()) * 100.
        denominator = self.t_end.timestamp() - self.t_start.timestamp()
        return int(numerator / denominator)

    def run(self):
        t_current = self.t_start
        p_current = 0

        while t_current <= self.t_end:
            # システム時刻の通知
            self.updateSystemTime.emit(
                t_current.strftime(self.time_format),
                self.get_progress(t_current)
            )

            if t_current in self.ser_tick.index:
                p_current = self.ser_tick.at[t_current]
                self.updateTickPrice.emit(
                    t_current.strftime(self.time_format),
                    p_current
                )
                # データフレームへデータを追加
                self.df.at[t_current, 'Price'] = p_current

            # 時刻を１秒進める
            t_current += self.t_second

        self.threadFinished.emit(self.df)
