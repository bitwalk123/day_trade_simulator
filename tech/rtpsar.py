import numpy as np
import pandas as pd


class RealTimePSAR:
    """
    Realtime Parabolic SAR
    """
    __version__ = '1.1.0'

    def __init__(self, af_init=0.000, af_step=0.001, af_max=0.01):
        self.af_init = af_init
        self.af_step = af_step
        self.af_max = af_max

        # 保持しておく指標
        self.ep = 0
        self.ep_count = 0  # 同じ EP である回数

        # クラス内で使用するデータフレーム
        df = pd.DataFrame()
        df.index.name = 'Datetime'
        self.df = df.astype(float)

    def add(self, dt1: pd.Timestamp, price1: float) -> int:
        # データフレームの行数
        r = len(self.df)

        if r == 0:
            # 最初は時刻と中立トレンドを記録
            trend1 = 0
            ep1 = np.nan
            af1 = np.nan
            psar1 = np.nan
        else:
            # 一つ前のデータを取得
            dt0 = self.df.index[r - 1]
            price0 = self.df.loc[dt0, 'Price']
            trend0 = self.df.loc[dt0, 'TREND']
            ep0 = self.df.loc[dt0, 'EP']
            af0 = self.df.loc[dt0, 'AF']
            psar0 = self.df.loc[dt0, 'PSAR']

            if r == 1:
                trend1 = self.trend_from_prices(price0, price1)
                ep1 = price1
                af1 = self.af_init
                psar1 = price1
            elif trend0 == 0:
                # トレンドが中立の時
                trend1 = self.trend_from_prices(price0, price1)
                ep1 = ep0
                af1 = af0
                psar1 = self.update_psar(ep1, af1, psar0)
            elif self.cmp_psar(trend0, price1, psar0):
                # トレンド反転
                trend1 = trend0 * -1
                ep1 = price1
                af1 = self.af_init
                psar1 = ep0
            else:
                # 同一トレンド
                trend1 = trend0
                if self.cmp_ep(trend0, price1, ep0):
                    # EP と AF の更新
                    ep1, af1 = self.update_ep_af(price1, af0)
                else:
                    ep1 = ep0
                    af1 = af0
                psar1 = self.update_psar(ep1, af1, psar0)

        # データフレームに新たな行を追加
        self.df.loc[dt1, 'Price'] = price1
        self.df.loc[dt1, 'TREND'] = trend1
        self.df.loc[dt1, 'EP'] = ep1
        self.df.loc[dt1, 'AF'] = af1
        self.df.loc[dt1, 'PSAR'] = psar1

        # 保持しておく指標
        if self.ep == ep1:
            self.ep_count += 1
        else:
            self.ep = ep1
            self.ep_count = 0  # EP のカウンタをリセット
        self.df.loc[dt1, 'EPcount'] = self.ep_count

        # 現在のトレンドを返す
        return trend1

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

    def getPSAR(self) -> pd.DataFrame:
        """
        PSAR のデータフレームを返す
        :return: PSAR のデータフレーム
        """
        return self.df

    def getEP(self) -> float:
        """
        現在保持している EP の値を取得
        :return:
        """
        return self.ep

    def getEPcount(self) -> int:
        """
        現在保持している EP count の値を取得
        :return:
        """
        return self.ep_count

    @staticmethod
    def trend_from_prices(price0: float, price1: float) -> int:
        """
        p0 と p1 を比較してトレンドを返す。
        :param price0:
        :param price1:
        :return:
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
        :param price:
        :param af:
        :return:
        """
        # EP の更新
        ep_new = price

        # AF の更新
        if af < self.af_max - self.af_step:
            af_new = af + self.af_step
        else:
            af_new = self.af_max

        return ep_new, af_new

    def update_psar(self, ep: float, af: float, psar: float) -> float:
        """
        PSAR を AF で更新
        :param ep:
        :param af:
        :param psar:
        :return:
        """
        return psar + af * (ep - psar)
