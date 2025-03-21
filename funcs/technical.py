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
