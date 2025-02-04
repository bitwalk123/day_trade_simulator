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
    threadFinished = Signal(pd.DataFrame, list)
    updateProfit = Signal(dict)
    updateSystemTime = Signal(str)
    updateTickPrice = Signal(str, float)
    updateProgress = Signal(int)
    updateTrend = Signal(int)


class WorkerSimulator(QRunnable, SimulatorSignal):
    def __init__(self, dict_target: dict):
        super().__init__()
        # 時刻フォーマット用文字列
        self.time_format = '%H:%M:%S'

        # ティックデータ
        self.df_tick = dict_target['tick']
        # 1 分足の OHLC データ
        self.df_ohlc_1m = dict_target['1m']

        # 取引時間
        self.date_str = dict_target['date_format']
        self.t_start = pd.to_datetime('%s 09:00:00' % self.date_str)
        self.t_end_1h = pd.to_datetime('%s 11:29:50' % self.date_str)
        self.t_start_2h = pd.to_datetime('%s 12:30:00' % self.date_str)
        self.t_end_2h = pd.to_datetime('%s 15:24:50' % self.date_str)
        self.t_end = pd.to_datetime('%s 15:31:00' % self.date_str)

        # 呼値
        self.price_delta_min = dict_target['price_delta_min']

        # 売買単位
        self.unit = dict_target['unit']

        # 取引オブジェクト
        self.trader = Trader(self.unit)

        # シミュレータ用時間定数
        self.t_second = datetime.timedelta(seconds=1)  # 1 秒
        self.t_minute = datetime.timedelta(minutes=1)  # 1 分

    def getTimeRange(self):
        return self.t_start.timestamp(), self.t_end.timestamp()

    def run(self):
        t_current = self.t_start
        p_current = 0

        trend = 0
        period = 0
        diff = 0

        while t_current <= self.t_end:
            ###################################################################
            ### 前処理
            # シミュレータ向けの処理

            # システム時刻の通知
            self.updateSystemTime.emit(
                t_current.strftime(self.time_format)
            )

            # ティックデータがあれば通知
            tick_price = self.find_tick_data(t_current)
            if not np.isnan(tick_price):
                p_current = tick_price

            ###
            ###################################################################

            if t_current <= self.t_end_1h or (self.t_start_2h <= t_current <= self.t_end_2h):
                # =============================================================
                # （アプリの）取引時間内
                # =============================================================
                if t_current.second == 1:
                    # ---------------------------------------------------------
                    # ジャスト 1 秒の時
                    # ---------------------------------------------------------
                    # 1 秒前（すなわち 0 秒の時）の PSAR トレンド情報を取得
                    t_prev = t_current - self.t_second
                    trend, period, diff = self.find_psar_trend(t_prev)
                    if np.isnan(trend):
                        # trend が NaN でなければ
                        # 取引オブジェクトが保持するトレンドを更新
                        trend = self.trader.getTrend()

                    # PSAR トレンド判定
                    if self.trader.getTrend() != trend:
                        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                        # トレンドが異なる場合（トレンド反転）
                        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                        # 取引オブジェクトが保持しているトレンドの更新
                        self.trader.setTrend(trend)

                        # 建玉返済
                        self.sessionClosePos(t_current, p_current, '返済（トレンド反転）')
                        # すぐさま反対売買（ドテン売買）はしない。
                    else:
                        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                        # トレンドが同一の場合
                        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                        if 0 < diff:
                            # トレンド開始後の差額がプラスの時のみ新たな建玉を取得。
                            note = '新規建玉@period=%d' % period
                            # 建玉取得
                            self.sessionOpenPos(t_current, p_current, note)
                        else:
                            # 損益評価
                            self.eval_profit(t_current, p_current)
                else:
                    # ---------------------------------------------------------
                    # ジャスト 1 秒以外の時
                    # ---------------------------------------------------------
                    # 損益評価
                    self.eval_profit(t_current, p_current)
            else:
                # =============================================================
                #  （アプリの）取引時間外
                # =============================================================
                # 建玉返済
                self.sessionClosePos(t_current, p_current, '強制返済')

            ###################################################################
            ### 後処理
            # 収益の更新
            dict_update = {
                '建玉価格': self.trader.getPrice(),
                '売買': self.trader.getPosition(),
                '含み損益': self.trader.getProfit(p_current),
                '最大含み益': self.trader.getProfitMax(),
                '合計損益': self.trader.getTotal(),
            }
            self.updateProfit.emit(dict_update)

            # 進捗を更新
            self.updateProgress.emit(t_current.timestamp())

            # 時刻を１秒進める
            t_current += self.t_second
            ###
            ###################################################################

        self.trader.calcProfitTotal()
        df_order = self.trader.getOrderHistory()
        column_format = self.trader.getColumnFormat()
        # スレッド処理の終了を通知
        self.threadFinished.emit(df_order, column_format)

    def eval_profit(self, t_current, p_current):
        pass

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

    def sessionOpenPos(self, ts, price, note='') -> bool:
        if not self.trader.hasPosition():
            transaction = dict()
            self.trader.openPosition(ts, price, transaction, note)
            return True
        else:
            return False

    def sessionClosePos(self, ts, price, note='') -> bool:
        if self.trader.hasPosition():
            transaction = dict()
            self.trader.closePosition(ts, price, transaction, note)
            return True
        else:
            return False
