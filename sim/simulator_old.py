import datetime

import numpy as np
import pandas as pd
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)

from sim.trader import Trader
from structs.app_enum import SimulationMode


class SimulatorSignal(QObject):
    threadFinished = Signal(pd.DataFrame, list, SimulationMode, dict)
    updateProfit = Signal(dict)
    updateSystemTime = Signal(str)
    updateTickPrice = Signal(str, float)
    updateProgress = Signal(int)
    updateTrend = Signal(int)


class WorkerSimulator(QRunnable, SimulatorSignal):
    def __init__(self, dict_target: dict, params: dict, mode: SimulationMode):
        super().__init__()
        self.dict_target = dict_target
        self.params = params
        self.mode = mode

        self.level_losscut_1 = None
        self.level_losscut_2 = None
        self.level_secure_1 = None
        self.threshold_profit_1 = None

        # 時刻フォーマット用文字列
        self.time_format = '%H:%M:%S'

        # 取引時間
        self.date_str = dict_target['date_format']
        self.t_start = pd.to_datetime('%s 09:00:00' % self.date_str)
        self.t_end_1h = pd.to_datetime('%s 11:29:50' % self.date_str)
        self.t_start_2h = pd.to_datetime('%s 12:30:00' % self.date_str)
        self.t_end_2h = pd.to_datetime('%s 15:24:50' % self.date_str)
        self.t_end = pd.to_datetime('%s 15:31:00' % self.date_str)

        # シミュレータ用時間定数
        self.t_second = datetime.timedelta(seconds=1)  # 1 秒
        self.t_minute = datetime.timedelta(minutes=1)  # 1 分

        # ティックデータ
        self.df_tick = dict_target['tick']
        # 1 分足の OHLC データ
        self.df_ohlc_1m = dict_target['1m']

        # 呼値
        self.price_delta_min = dict_target['price_delta_min']

        # 売買単位
        self.unit = dict_target['unit']

        # 取引オブジェクト
        self.trader = Trader(self.unit)

        # 利確・損切パラメータの設定
        self.setting_params(params)

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
            if self.mode == SimulationMode.NORMAL:
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
                self.loopMain(t_current, p_current)
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
            if self.mode == SimulationMode.NORMAL:
                self.updateProfit.emit(dict_update)

            # 進捗を更新
            if self.mode == SimulationMode.NORMAL:
                self.updateProgress.emit(t_current.timestamp())

            # 時刻を１秒進める
            t_current += self.t_second
            ###
            ###################################################################

        self.trader.calcProfitTotal()
        df_order = self.trader.getOrderHistory()
        column_format = self.trader.getColumnFormat()

        # --------------------
        # スレッド処理の終了を通知
        # --------------------
        result = dict()
        # 最適条件探索時
        if self.mode == SimulationMode.EXPLORE:
            result['code'] = self.dict_target['code']
            result['date'] = self.dict_target['date_format']
            #result['params'] = self.params
            for key in self.params.keys():
                result[key] = self.params[key]
            result['total'] = self.trader.getTotal()
        self.threadFinished.emit(df_order, column_format, self.mode, result)

    def loopMain(self, t_current, p_current):
        if t_current.second == 1:
            # -----------------------------------------------------------------
            # 【ジャスト 1 秒の時】
            # 理想的には HH:MM:00 に新しい 1 分足の OHLC の情報が流れ込み、
            # その情報を元に「平均足」、Prabolic SAR が算出され、その後に売買判定が行われる。
            # 現実的には、特に終盤になると VBA の実環境では 1 秒遅れになる場合が多いので、
            # シミュレーション環境では、はじめから 1 秒遅れるものとして実行する。
            # -----------------------------------------------------------------
            # 1 秒前（すなわち 0 秒の時）の PSAR トレンド情報を取得
            t_prev = t_current - self.t_second
            trend, period, diff = self.find_psar_trend(t_prev)
            if np.isnan(trend):
                # trend が NaN でなければ
                # 取引オブジェクトが保持するトレンドを更新
                trend = self.trader.getTrend()

            # PSAR トレンド判定
            if self.trader.getTrend() != trend:
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # トレンドが異なる場合（トレンド反転）
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # 取引オブジェクトが保持しているトレンドの更新
                self.trader.setTrend(trend)

                # 建玉返済
                self.sessionClosePos(t_current, p_current, '返済（トレンド反転）')
                # すぐさま反対売買（ドテン売買）はしない。
            else:
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # トレンドが同一の場合
                # 建玉を取得するタイミングは、当面はここだけに限定する
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                if period < self.period_max and 0 < diff:
                    # トレンド開始後の差額がプラスの時のみ新たな建玉を取得。
                    note = '新規建玉@period=%d' % period
                    # 建玉取得
                    self.sessionOpenPos(t_current, p_current, note)
                else:
                    # 損益評価
                    self.eval_profit(t_current, p_current)
        else:
            # -----------------------------------------------------------------
            # 【ジャスト 1 秒以外の時】
            # -----------------------------------------------------------------
            # 損益評価
            self.eval_profit(t_current, p_current)

    def eval_profit(self, t_current, p_current):
        profit = self.trader.getProfit(p_current)
        # ========
        #  損　切
        # ========
        # 損切１
        # PSAR トレンド内で一度も含み益がプラスになっていない時の損切レベル
        if profit < self.level_losscut_1 and 0 == self.trader.getProfitMax():
            if self.sessionClosePos(t_current, p_current, '損切１'):
                return
        # 損切２
        # PSAR トレンド内で最大含み益がプラスになっている時の損切レベル
        if profit < self.level_losscut_2 and 0 < self.trader.getProfitMax():
            if self.sessionClosePos(t_current, p_current, '損切２'):
                return

        # ========
        #  利　確
        # ========
        profit_lower = self.trader.getProfitMax() * self.threshold_profit_1 / 10.0
        # 利確１
        if self.level_secure_1 < self.trader.getProfitMax() and profit < profit_lower:
            if self.sessionClosePos(t_current, p_current, '利確１'):
                return

    def find_tick_data(self, t_current):
        """
        現在時刻のティックデータがあれば通知
        :param t_current:
        :return:
        """
        if t_current in self.df_tick.index:
            p_current = self.df_tick.at[t_current, 'Price']

            # 現在値詳細時刻と現在値を通知
            if self.mode == SimulationMode.NORMAL:
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
                if self.mode == SimulationMode.NORMAL:
                    self.updateTrend.emit(trend)

        return trend, period, diff

    def sessionOpenPos(self, ts, price, note='') -> bool:
        """
        建玉の取得
        :param ts:
        :param price:
        :param note:
        :return:
        """
        if not self.trader.hasPosition():
            transaction = dict()
            self.trader.openPosition(ts, price, transaction, note)
            return True
        else:
            return False

    def sessionClosePos(self, ts, price, note='') -> bool:
        """
        建玉の返済
        :param ts:
        :param price:
        :param note:
        :return:
        """
        if self.trader.hasPosition():
            transaction = dict()
            self.trader.closePosition(ts, price, transaction, note)
            return True
        else:
            return False

    def setting_params(self, params: dict):
        """
        シミュレーション・パラメータの設定
        :return:
        """
        # ---------------------------------------------------------------------
        # エントリー可能な最大 period in PSAR
        # ここで設定した数より大きい period で diff が正になっても
        # 大きくは伸びないと仮定してエントリを諦める
        # ---------------------------------------------------------------------
        self.period_max = params['period_max']

        # ---------------------------------------------------------------------
        # 利確・損切レベル
        # ---------------------------------------------------------------------
        # 呼値×売買単位
        block = self.price_delta_min * self.unit

        # ロスカット・レベル１
        # PSAR トレンド内で一度も含み益がプラスになっていない時の損切レベル
        factor_losscut_1 = params['factor_losscut_1']
        self.level_losscut_1 = -1 * block * factor_losscut_1

        # ロスカット・レベル２
        # PSAR トレンド内で最大含み益がプラスになっている時の損切レベル
        factor_losscut_2 = params['factor_losscut_2']
        self.level_losscut_2 = -1 * block * factor_losscut_2

        # 利確検討最低価格１
        factor_profit_1 = params['factor_profit_1']
        self.level_secure_1 = block * factor_profit_1
        # 利確しきい値１
        # 最大含み損にしきい値を乗じた値を下回れば利確する。
        self.threshold_profit_1 = params['threshold_profit_1']
