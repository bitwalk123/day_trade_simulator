"""
Parabolic SAR シミュレータ

【特徴】
 トレンド反転の後、エントリのタイミングを EP の更新回数 5 で評価
"""
import datetime

import pandas as pd
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)

from tech.rtpsar import RealTimePSAR
from sim.posman import PositionManager


class SimulatorSignal(QObject):
    positionOpen = Signal(dict)
    positionClose = Signal(float)
    simulationCompleted = Signal(dict)  # auto-simulation 用
    threadFinished = Signal(dict)
    updateProfit = Signal(dict)
    updateSystemTime = Signal(str, int)
    updateTickPrice = Signal(str, float, int)


class WorkerSimulator(QRunnable, SimulatorSignal):
    def __init__(self, dict_param: dict):
        super().__init__()

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # シミュレーション用データ＆パラメータ（はじめ）

        # ログデータ
        self.ser_tick: pd.Series = dict_param['tick']

        # 日付文字列
        self.date_str = date_str = dict_param['date']

        # 売買単位
        unit = dict_param['unit']

        # 呼び値
        price_nominal = dict_param['price_nominal']

        # 損切（ロスカット）機能が有効か否か
        self.flag_losscut = dict_param['flag_losscut']

        if self.flag_losscut:
            # 損切（ロスカット）因数
            factor_losscut = dict_param['factor_losscut']
            self.losscut = factor_losscut / price_nominal
            # print('losscut', self.losscut)
        else:
            self.losscut = -100000.0  # バカヨケ

        # print('損切機能', self.flag_losscut, '損切（ロスカット）', self.losscut)

        # Parabolic SAR 関連パラメータ（加速度因数）
        af_init = dict_param['af_init']
        af_step = dict_param['af_step']
        af_max = dict_param['af_max']

        # シミュレーション用データ＆パラメータ（おわり）
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

        # 取引時間
        self.t_start = pd.to_datetime('%s 09:00:00' % date_str)
        self.t_end = pd.to_datetime('%s 15:30:00' % date_str)

        # 時刻フォーマット用文字列
        self.time_format = '%H:%M:%S'

        # シミュレータ用時間定数
        self.t_second = datetime.timedelta(seconds=1)  # 1 秒（インクリメント用）

        # トレンド内でエントリしたかどうか？
        self.flag_entry = False

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # 🧬 RealTimePSAR クラスのインスタンス
        #
        self.psar = RealTimePSAR(af_init, af_step, af_max)
        #
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # 🧬 建玉管理クラスのインスタンス
        #
        self.posman = PositionManager(unit)
        #
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

    def get_progress(self, t) -> int:
        """
        現在時刻から進捗度(%)を算出
        """
        # 分子
        numerator = (t.timestamp() - self.t_start.timestamp()) * 100.0
        # 分母
        denominator = self.t_end.timestamp() - self.t_start.timestamp()

        return int(numerator / denominator)

    def run(self):
        """
        シミュレータ本体
        """
        # 時刻、株価の初期化
        t_current = self.t_start
        p_current = 0

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # 時刻ループ（はじめ）
        while t_current < self.t_end:
            # -----------------------------------------------------------------
            # 🧿 システム時刻と進捗を通知
            self.updateSystemTime.emit(
                t_current.strftime(self.time_format),
                self.get_progress(t_current)
            )
            # -----------------------------------------------------------------

            # ループの時刻がログの時刻列に存在すれば現在価格を更新
            if t_current in self.ser_tick.index:
                # 現在価格の取得
                p_current = self.ser_tick.at[t_current]

                # Parabolic SAR の算出
                trend = self.psar.add(t_current, p_current)

                # -------------------------------------------------------------
                # 🧿 現在時刻＆現在価格の更新を通知
                self.updateTickPrice.emit(
                    t_current.strftime(self.time_format),
                    p_current,
                    trend
                )
                # -------------------------------------------------------------

                # =============================================================
                #  トレンド反転の判定処理（はじめ）
                if self.posman.getTrend() != trend:
                    # 建玉を持って入れば返済
                    if self.posman.hasPosition():
                        self.position_close(t_current, p_current)

                    # トレンドを更新
                    self.posman.setTrend(trend)

                    # エントリ・フラグをリセット
                    self.flag_entry = False

                elif self.flag_entry is False:
                    # -------------
                    # 未エントリの場合
                    # -------------
                    if self.psar.getEPupd() > 5:
                        # +++++++++++++++++++++++++++++++++++++++++++++
                        # 暫定エントリ条件
                        # PSAR の EP が 1 回でも更新されていれば建玉を取得する
                        # +++++++++++++++++++++++++++++++++++++++++++++
                        self.position_open(t_current, p_current)
                        # エントリ・フラグを立てる
                        self.flag_entry = True
                else:
                    # エントリしている ＝ 建玉を持っている
                    # 利確・損切
                    pass

                #  トレンド反転の判定処理（おわり）
                # =============================================================

            # 含み益の評価
            if self.posman.hasPosition():
                self.eval_profit(t_current, p_current)

            # 時刻を１秒進める
            t_current += self.t_second

        # 時刻ループ（おわり）
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

        # 建玉を持って入れば返済
        if self.posman.hasPosition():
            self.position_close(t_current, p_current, '強制（大引け）')
            # 含み益の評価
            self.eval_profit(t_current, p_current)

        dict_result = dict()
        dict_result['date']= self.date_str
        dict_result['tick'] = self.psar.getPSAR()
        dict_result['profit'] = self.posman.getProfitHistory()
        dict_result['order'] = self.posman.getOrderHistory()
        dict_result['column_format'] = self.posman.getColFormatOrder()
        dict_result['total'] = self.posman.getTotal()

        # ---------------------------------------------------------------------
        # 🧿 スレッド処理の終了を通知
        self.threadFinished.emit(dict_result)
        #
        # 🧿 シミュレーション処理の終了を通知（auto-simulation 用シグナル）
        self.simulationCompleted.emit(dict_result)
        # ---------------------------------------------------------------------

    def position_close(self, t_current, p_current, note: str = ''):
        """
        建玉管理インスタンスが保持しているトレンドに従って建玉を返済
        :param t_current:
        :param p_current:
        :param note:
        :return:
        """
        total = self.posman.posClose(t_current, p_current, note)
        # ---------------------------------------------------------------------
        # 🧿 建玉を返却したことを通知
        self.positionClose.emit(total)
        # ---------------------------------------------------------------------

    def position_open(self, t_current, p_current, note: str = ''):
        """
        建玉管理インスタンスが保持しているトレンドに従って建玉を持つ
        :param t_current:
        :param p_current:
        :param note:
        :return:
        """
        dict_position = self.posman.posOpen(t_current, p_current, note)
        # ---------------------------------------------------------------------
        # 🧿 建玉を持ったことを通知
        self.positionOpen.emit(dict_position)
        # ---------------------------------------------------------------------

    def eval_profit(self, t_current, p_current):
        """
        建玉管理インスタンスが保持しているトレンドに従って含み益を評価
        :param t_current:
        :param p_current:
        :return:
        """
        dict_profit = self.posman.evalProfit(t_current, p_current)
        # ---------------------------------------------------------------------
        # 🧿 更新された含み益を通知
        self.updateProfit.emit(dict_profit)
        # ---------------------------------------------------------------------

        # 損切（ロスカット）
        if self.flag_losscut:
            self.test_losscut(t_current, p_current, dict_profit)

    def test_losscut(self, t_current, p_current, dict_profit):
        if dict_profit['profit'] < 0 and self.losscut < self.psar.getPricePSARDelta(p_current):
            self.position_close(t_current, p_current, '損切')
