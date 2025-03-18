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
    def __init__(self, dict_param: dict):
        super().__init__()

        # =====================================================================
        # シミュレーション用データ＆パラメータ（はじめ）

        # ログデータ
        self.ser_tick: pd.Series = dict_param['tick']

        # 日付文字列
        date_str = dict_param['date']

        # Parabolic SAR 関連パラメータ（加速度因数）
        self.af_init = dict_param['af_init']
        self.af_step = dict_param['af_step']
        self.af_max = dict_param['af_max']

        # シミュレーション用データ＆パラメータ（おわり）
        # =====================================================================

        # 取引時間
        self.t_start = pd.to_datetime('%s 09:00:00' % date_str)
        self.t_end = pd.to_datetime('%s 15:30:00' % date_str)

        # 時刻フォーマット用文字列
        self.time_format = '%H:%M:%S'

        # シミュレータ用時間定数
        self.t_second = datetime.timedelta(seconds=1)  # 1 秒（インクリメント用）

        # プロット用データフレーム
        dict_columns = {
            'Price': [],
            'TREND': [],
            'EP': [],
            'AF': [],
            'PSAR': [],
        }
        df = pd.DataFrame.from_dict(dict_columns)  # 空のデータフレーム
        df.index.name = 'Datetime'  # インデックス名
        self.df = df.astype(float)  # セル全てが float とする

    def get_progress(self, t) -> int:
        """
        現在時刻から進捗度(%)を算出
        :param t:
        :return:
        """
        numerator = (t.timestamp() - self.t_start.timestamp()) * 100.
        denominator = self.t_end.timestamp() - self.t_start.timestamp()

        return int(numerator / denominator)

    def run(self):
        """
        シミュレータ本体
        :return:
        """
        t_current = self.t_start

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # 時刻ループ（はじめ）
        while t_current <= self.t_end:
            # ---------------------
            #  システム時刻と進捗の通知
            # ---------------------
            self.updateSystemTime.emit(
                t_current.strftime(self.time_format),
                self.get_progress(t_current)
            )

            # ループの時刻がログの時刻列に存在すれば現在価格を更新
            if t_current in self.ser_tick.index:
                # 現在価格の取得
                p_current = self.ser_tick.at[t_current]

                # データフレームへデータを追加
                self.df.at[t_current, 'Price'] = p_current

                # --------------------------
                #  現在時刻＆現在価格の更新を通知
                # --------------------------
                self.updateTickPrice.emit(
                    t_current.strftime(self.time_format),
                    p_current
                )

            # 時刻を１秒進める
            t_current += self.t_second
        # 時刻ループ（おわり）
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

        # ---------------------
        #  スレッド処理の終了を通知
        # ---------------------
        self.threadFinished.emit(self.df)
