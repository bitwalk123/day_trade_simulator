import json

import pandas as pd
import yfinance as yf

from func.common import (
    get_csv_ohlc_name,
    get_csv_tick_name,
)

from func.tide import (
    get_dates,
)
from structs.res import AppRes


def get_ohlc(res: AppRes, target: dict) -> pd.DataFrame:
    """
    OHLC データをデータフレームで取得
    :param res:
    :param target:
    :return:
    """
    # OHLCのファイル名（CSV形式）
    file_ohlc = get_csv_ohlc_name(res, target)
    df = pd.read_csv(file_ohlc)
    df.index = pd.to_datetime(
        ['%s %s' % (df['日付'].iloc[r], df['時刻'].iloc[r]) for r in range(len(df))]
    )
    df.index.name = 'Datetime'

    list_col_0 = ['始値', '高値', '安値', '終値', '出来高', 'TREND', 'EP', 'AF', 'PSAR']
    list_col_1 = ['Open', 'High', 'Low', 'Close', 'Volume', 'TREND', 'EP', 'AF', 'PSAR']
    df0 = df[list_col_0].copy()
    df0.columns = list_col_1
    return df0


def get_tick(res: AppRes, target: dict) -> pd.DataFrame:
    file_tick = get_csv_tick_name(res, target)
    df = pd.read_csv(file_tick)
    df.index = pd.to_datetime(
        ['%s %s' % (target['date2'], df['時刻'].iloc[r]) for r in range(len(df))]
    )
    df.index.name = 'Datetime'
    ser = df['株価'].copy()
    ser.name = 'Price'
    return pd.DataFrame(ser)


def get_ohlc_from_yahoo(target: dict) -> pd.DataFrame:
    """
    １分足データを取得
    :param target:
    :return:
    """
    ticker = yf.Ticker(target["symbol"])
    start, end = get_dates(target["date"])
    return ticker.history(
        period='1d',
        interval=target["interval"],
        start=start,
        end=end,
    )


def read_json(jsonfile: str) -> dict:
    """
    指定された JSON ファイルを読み込む
    :param jsonfile:
    :return:
    """
    with open(jsonfile) as f:
        dict_contents = json.load(f)
    return dict_contents
