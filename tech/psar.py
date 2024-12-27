import pandas as pd
import numpy as np

P_HIGH = 1
P_LOW = 2
P_CLOSE = 3
TREND = 5
EP = 6
AF = 7
PSAR = 8

AF_INIT = 0.02
AF_STEP = 0.02
AF_MAX = 0.2


def initialize(df: pd.DataFrame) -> pd.DataFrame:
    list_head_base = ['Open', 'High', 'Low', 'Close', 'Volume']

    df = df[list_head_base].copy()
    df['Trend'] = np.nan
    df['EP'] = np.nan
    df['AF'] = np.nan
    df['PSAR'] = np.nan

    return df


def calc_PSAR0(df: pd.DataFrame, i: int):
    # Trend
    if df.iloc[i, P_CLOSE] > df.iloc[i - 1, P_CLOSE]:
        val_TREND = 1
    else:
        val_TREND = -1
    df.iloc[i, TREND] = val_TREND

    # EP
    if val_TREND == 1:
        val_EP = df.iloc[i, P_HIGH]
    else:
        val_EP = df.iloc[i, P_LOW]
    df.iloc[i, EP] = val_EP

    # AF
    df.iloc[i, AF] = AF_INIT

    # PSAR
    if val_TREND == 1:
        val_PSAR = df.iloc[i, P_HIGH]
    else:
        val_PSAR = df.iloc[i, P_LOW]
    df.iloc[i, PSAR] = val_PSAR


def calc_PSAR(df: pd.DataFrame, i: int):
    # Trend
    if df.iloc[i - 1, TREND] == 1:
        if df.iloc[i - 1, PSAR] > df.iloc[i, P_LOW]:
            val_TREND = -1
        else:
            val_TREND = 1
    else:
        if df.iloc[i - 1, PSAR] < df.iloc[i, P_HIGH]:
            val_TREND = 1
        else:
            val_TREND = -1
    df.iloc[i, TREND] = val_TREND

    # EP
    if val_TREND == 1:
        if df.iloc[i - 1, PSAR] > df.iloc[i, P_LOW]:
            val_EP = df.iloc[i, P_LOW]
        elif df.iloc[i, P_HIGH] > df.iloc[i - 1, EP]:
            val_EP = df.iloc[i, P_HIGH]
        else:
            val_EP = df.iloc[i - 1, EP]
    else:
        if df.iloc[i - 1, PSAR] < df.iloc[i, P_HIGH]:
            val_EP = df.iloc[i, P_HIGH]
        elif df.iloc[i, P_LOW] < df.iloc[i - 1, EP]:
            val_EP = df.iloc[i, P_LOW]
        else:
            val_EP = df.iloc[i - 1, EP]
    df.iloc[i, EP] = val_EP

    # AF
    if val_TREND != df.iloc[i - 1, TREND]:
        val_AF = AF_INIT
    else:
        if val_EP != df.iloc[i - 1, EP] and df.iloc[i - 1, AF] < AF_MAX:
            val_AF = df.iloc[i - 1, AF] + AF_STEP
        else:
            val_AF = df.iloc[i - 1, AF]
    df.iloc[i, AF] = val_AF

    # PSAR
    if val_TREND == df.iloc[i - 1, TREND]:
        val_PSAR = df.iloc[i - 1, PSAR] + val_AF * (val_EP - df.iloc[i - 1, PSAR])
    else:
        val_PSAR = df.iloc[i - 1, EP]
    df.iloc[i, PSAR] = val_PSAR
