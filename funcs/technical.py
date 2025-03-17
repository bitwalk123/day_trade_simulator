import numpy as np
import pandas as pd


def calc_robust_bollinger(df: pd.DataFrame, period: int):
    r_last = len(df)
    r1 = 0
    df['Median'] = np.nan
    df['Q1'] = np.nan
    df['Q3'] = np.nan
    df['Lower'] = np.nan
    df['Upper'] = np.nan
    while r1 < r_last - period:
        r2 = r1 + period
        df1 = df.iloc[r1:r2].copy()
        med = np.median(df1['Close'])
        q3, q1 = np.percentile(df1['Close'], [75, 25])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)  # 下限を設定
        upper_bound = q3 + (1.5 * iqr)  # 上限を設定
        name_index = df.index[r2]
        df.at[name_index, 'Median'] = med
        df.at[name_index, 'Q1'] = q1
        df.at[name_index, 'Q3'] = q3
        df.at[name_index, 'Lower'] = lower_bound
        df.at[name_index, 'Upper'] = upper_bound
        r1 += 1


def psar(ohlc: pd.DataFrame, iaf: float = 0.02, maxaf: float = 0.2) -> dict:
    length = len(ohlc)
    high = ohlc['High'].tolist()
    low = ohlc['Low'].tolist()
    close = ohlc['Close'].tolist()

    psar = close[0:len(close)]
    psarbull = [None] * length
    psarbear = [None] * length

    bull = True
    af = iaf
    ep = low[0]
    price_high = high[0]
    price_low = low[0]

    for i in range(2, length):
        if bull:
            psar[i] = psar[i - 1] + af * (price_high - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (price_low - psar[i - 1])
        reverse = False

        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = price_high
                price_low = low[i]
                af = iaf
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = price_low
                price_high = high[i]
                af = iaf

        if not reverse:
            if bull:
                if high[i] > price_high:
                    price_high = high[i]
                    af = min(af + iaf, maxaf)
                if low[i - 1] < psar[i]:
                    psar[i] = low[i - 1]
                if low[i - 2] < psar[i]:
                    psar[i] = low[i - 2]
            else:
                if low[i] < price_low:
                    price_low = low[i]
                    af = min(af + iaf, maxaf)
                if high[i - 1] > psar[i]:
                    psar[i] = high[i - 1]
                if high[i - 2] > psar[i]:
                    psar[i] = high[i - 2]

        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]

    return {
        'bear': np.array(psarbear, dtype='float64'),
        'bull': np.array(psarbull, dtype='float64'),
    }


class RealTimePSAR:
    def __init__(self, af_init=0.001, af_step=0.001, af_max=0.04):
        self.af_init = af_init
        self.af_step = af_step
        self.af_max = af_max
        df = pd.DataFrame()
        df.index.name = 'Datetime'
        self.df = df.astype(float)

    def add(self, t1, p1):
        r = len(self.df)
        self.df.loc[t1, 'Price'] = p1

        if r == 0:
            self.add_psar(t1, 0, np.nan, np.nan, np.nan)
            return

        t0 = self.df.index[r - 1]
        p0 = self.df.loc[t0, 'Price']

        if r == 1:
            trend1 = self.trend_from_prices(p0, p1)
            self.trend_reversal(t1, p1, trend1, p1)
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
