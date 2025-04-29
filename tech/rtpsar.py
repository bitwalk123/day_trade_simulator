import numpy as np
import pandas as pd


class RealTimePSAR:
    """
    Realtime Parabolic SAR
    検証用クラス
    """
    __version__ = '1.4.0'

    def __init__(self, af_init=0.000, af_step=0.001, af_max=0.01, q=50):
        self.af_init = af_init
        self.af_step = af_step
        self.af_max = af_max

        # ---------------------------------------------------------------------
        # 【注意】
        #  VBAの数値型変数はNullにならない。
        #  https://www.relief.jp/docs/vba-check-if-isnull-numeric-variable.html
        #  VBA への移植するためには、最終的に np.nan を使用しないコーディングにした方が良い
        # ---------------------------------------------------------------------

        # 一つ前の値 (6)
        self.dt0 = 0
        self.price0 = 0
        self.trend0 = 0
        self.ep0 = 0
        self.af0 = -1  # AF は 0 以上の実数
        self.psar0 = 0

        # トレンド反転したときの株価
        self.baseline = 0

        # トレンド ＆ EP 更新モニター
        self.n_trend = 1
        self.n_ep_update = 0

        # 双曲線の補助線（ロスカット用）
        self.r = 0
        self.p = 0
        self.q = q
        self.x = 0

        # クラス内で使用するデータフレーム
        df = pd.DataFrame()
        df.index.name = 'Datetime'
        self.df = df.astype(float)

    def add(self, dt1: pd.Timestamp, price1: float) -> int:
        # データフレームの行数
        r = len(self.df)

        if r == 0:
            # -----------------------------------------------------------------
            # 【PSAR 最初の処理】
            #  比較対象がないので、時刻と中立トレンドを記録
            # -----------------------------------------------------------------
            trend1 = 0
            # ---------------------------------------------------------
            # 【パラメータ更新】
            #  中立の場合は nan
            # ---------------------------------------------------------
            ep1 = 0
            af1 = -1
            psar1 = 0
        else:
            if r == 1:
                # -------------------------------------------------------------
                # 【PSAR 2番目の処理】
                #  前の株価と差を確認して、差があればトレンド開始
                # -------------------------------------------------------------
                trend1 = self.trend_from_prices(self.price0, price1)
                if trend1 == 0:
                    # ---------------------------------------------------------
                    # 【パラメータ初期値】
                    #  中立の場合は nan
                    # ---------------------------------------------------------
                    ep1 = 0
                    af1 = -1
                    psar1 = 0

                    # トレンド反転したときの株価
                    self.baseline = np.nan
                else:
                    # ---------------------------------------------------------
                    # 【パラメータ初期値】
                    #  中立から最初のトレンド
                    # ---------------------------------------------------------
                    ep1 = price1
                    af1 = self.af_init
                    psar1 = price1

                    # トレンド反転したときの株価
                    self.baseline = price1

                    # トレンド ＆ EP 更新モニター
                    self.n_trend = 1
                    self.n_ep_update = 0
            elif self.trend0 == 0:
                # -------------------------------------------------------------
                # 【トレンドが中立の時】
                #  ストップ安・高になってしまった場合などを想定
                # -------------------------------------------------------------
                trend1 = self.trend_from_prices(self.price0, price1)
                if trend1 == 0:
                    # ---------------------------------------------------------
                    # 【パラメータ初期値】
                    #  中立の場合は nan
                    # ---------------------------------------------------------
                    ep1 = 0
                    af1 = -1
                    psar1 = 0

                    # トレンド反転したときの株価
                    self.baseline = 0
                else:
                    # ---------------------------------------------------------
                    # 【パラメータ初期値】
                    #  中立から最初のトレンド
                    # ---------------------------------------------------------
                    ep1 = price1
                    af1 = self.af_init
                    psar1 = price1

                    # トレンド反転したときの株価
                    self.baseline = price1

                    # トレンド ＆ EP 更新モニター
                    self.n_trend = 1
                    self.n_ep_update = 0
            elif self.cmp_psar(self.trend0, price1, self.psar0):
                # _/_/_/_/_/_/
                # トレンド反転
                # _/_/_/_/_/_/
                trend1 = self.trend0 * -1

                # -------------------------------------------------------------
                # 【パラメータ初期値】
                # トレンド反転後の最初のトレンド
                # -------------------------------------------------------------
                ep1 = price1
                af1 = self.af_init
                psar1 = self.ep0

                # トレンド反転したときの株価
                self.baseline = price1

                # トレンド ＆ EP 更新モニター
                self.n_trend = 1
                self.n_ep_update = 0

                # 双曲線の補助線
                self.p = price1
                self.r = (price1 - self.ep0) * self.q
                self.x = 0
            else:
                # 同一トレンド
                trend1 = self.trend0

                # トレンドモニター
                self.n_trend += 1

                # EP 更新するか？
                if self.cmp_ep(self.trend0, price1, self.ep0):
                    # EP と AF の更新
                    ep1, af1 = self.update_ep_af(price1, self.af0)

                    # EP 更新モニター
                    self.n_ep_update += 1
                else:
                    ep1 = self.ep0
                    af1 = self.af0

                psar1 = self.update_psar(ep1, af1, self.psar0)

        self.update_info(dt1, price1, trend1, ep1, af1, psar1)

        # 現在のトレンドを返す
        return trend1

    @staticmethod
    def cmp_ep(trend: int, price: float, ep: float) -> bool:
        if 0 < trend:
            if ep < price:
                return True
            else:
                return False
        else:
            if price < ep:
                return True
            else:
                return False

    @staticmethod
    def cmp_psar(trend: int, price: float, psar: float) -> bool:
        if 0 < trend:
            if price < psar:
                return True
            else:
                return False
        else:
            if psar < price:
                return True
            else:
                return False

    def getEPupd(self) -> int:
        return self.n_ep_update

    def getPSAR(self) -> pd.DataFrame:
        """
        PSAR のデータフレームを返す
        :return: PSAR のデータフレーム
        """
        return self.df

    @staticmethod
    def trend_from_prices(price0: float, price1: float) -> int:
        """
        price0 と price1 を比較してトレンドを返す。
        """
        if price0 < price1:
            return 1
        elif price1 < price0:
            return -1
        else:
            return 0

    def update_ep_af(self, price: float, af: float) -> tuple[float, float]:
        """
        EP（極値）と AF（加速因数）の更新
        """
        # EP の更新
        ep_new = price

        # AF の更新
        if af < self.af_max - self.af_step:
            af_new = af + self.af_step
        else:
            af_new = self.af_max

        return ep_new, af_new

    def update_info(self, dt, price, trend, ep, af, psar):
        self.dt0 = dt
        self.price0 = price
        self.trend0 = trend
        self.ep0 = ep
        self.af0 = af
        self.psar0 = psar

        # データフレームに新たな行を追加
        self.df.loc[dt, 'Price'] = price
        self.df.loc[dt, 'TREND'] = trend
        if ep > 0:
            self.df.loc[dt, 'EP'] = ep
        if af >= 0:
            self.df.loc[dt, 'AF'] = af
        if psar > 0:
            self.df.loc[dt, 'PSAR'] = psar
        if self.baseline > 0:
            self.df.loc[dt, 'Baseline'] = self.baseline

        # 双曲線の補助線
        if self.p > 0:
            try:
                self.df.loc[dt, 'Losscut'] = self.p - self.r / (self.x + self.q)
                self.x += 1
            except ZeroDivisionError:
                self.df.loc[dt, 'Losscut'] = np.nan
                print('ZeroDivisionError')

        # トレンド＆EP更新モニター
        self.df.loc[dt, 'TrendN'] = self.n_trend
        self.df.loc[dt, 'EPupd'] = self.n_ep_update

    @staticmethod
    def update_psar(ep: float, af: float, psar: float) -> float:
        """
        PSAR を AF で更新
        :param ep:
        :param af:
        :param psar:
        :return:
        """
        return psar + af * (ep - psar)
