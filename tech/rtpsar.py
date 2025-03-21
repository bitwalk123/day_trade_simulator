import numpy as np
import pandas as pd


class RealTimePSAR:
    """
    Realtime Parabolic SAR
    """
    def __init__(self, af_init=0.001, af_step=0.001, af_max=0.04):
        self.af_init = af_init
        self.af_step = af_step
        self.af_max = af_max
        # dateframe used in this class
        df = pd.DataFrame()
        df.index.name = 'Datetime'
        self.df = df.astype(float)

    def add(self, t1, p1) -> int:
        r = len(self.df)
        self.df.loc[t1, 'Price'] = p1

        if r == 0:
            self.add_psar(t1, 0, np.nan, np.nan, np.nan)
            return 0

        t0 = self.df.index[r - 1]
        p0 = self.df.loc[t0, 'Price']

        if r == 1:
            trend1 = self.trend_from_prices(p0, p1)
            self.trend_reversal(t1, p1, trend1, p1)

            return int(trend1)
        else:
            trend0 = self.df.loc[t0, 'TREND']
            ep0 = self.df.loc[t0, 'EP']
            af0 = self.df.loc[t0, 'AF']
            psar0 = self.df.loc[t0, 'PSAR']

            if 0 < trend0:
                if p1 < psar0:
                    trend1 = -1
                    self.trend_reversal(t1, p1, trend1, ep0)
                else:
                    trend1 = trend0
                    if ep0 < p1:
                        ep1 = p1
                        if af0 < self.af_max - self.af_step:
                            af1 = af0 + self.af_step
                        else:
                            af1 = self.af_max
                    else:
                        ep1 = ep0
                        af1 = af0
                    psar1 = psar0 + af1 * (ep1 - psar0)
                    self.add_psar(t1, trend1, ep1, af1, psar1)
            elif trend0 < 0:
                if psar0 < p1:
                    trend1 = 1
                    self.trend_reversal(t1, p1, trend1, ep0)
                else:
                    trend1 = trend0
                    if p1 < ep0:
                        ep1 = p1
                        if af0 < self.af_max - self.af_step:
                            af1 = af0 + self.af_step
                        else:
                            af1 = self.af_max
                    else:
                        ep1 = ep0
                        af1 = af0
                    psar1 = psar0 + af1 * (ep1 - psar0)
                    self.add_psar(t1, trend1, ep1, af1, psar1)
            else:
                trend1 = self.trend_from_prices(p0, p1)
                ep1 = ep0
                af1 = af0
                psar1 = psar0 + af1 * (ep1 - psar0)
                self.add_psar(t1, trend1, ep1, af1, psar1)

            return int(trend1)

    @staticmethod
    def trend_from_prices(p0, p1):
        if p0 < p1:
            trend = 1
        elif p1 < p0:
            trend = -1
        else:
            trend = 0
        return trend

    def trend_reversal(self, t, p, trend1, ep0):
        ep1 = p
        af1 = self.af_init
        psar1 = ep0
        self.add_psar(t, trend1, ep1, af1, psar1)

    def add_psar(self, t, trend, ep, af, psar):
        self.df.loc[t, 'TREND'] = trend
        self.df.loc[t, 'EP'] = ep
        self.df.loc[t, 'AF'] = af
        self.df.loc[t, 'PSAR'] = psar

    def get_df(self):
        return self.df
