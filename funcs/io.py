import json
import os

import pandas as pd
import yfinance as yf

from funcs.common import (
    get_csv_ohlc_name,
    get_csv_tick_name,
)

from funcs.tide import (
    get_dates,
)
from structs.res import AppRes


def get_ohlc(res: AppRes, target: dict, interval: str) -> pd.DataFrame:
    """
    OHLC データをデータフレームで取得
    :param res:
    :param target:
    :return:
    """
    # OHLCのファイル名（CSV形式）
    file_ohlc = get_csv_ohlc_name(res, target, interval)
    if os.path.isfile(file_ohlc):
        df = pd.read_csv(file_ohlc)
    else:
        return pd.DataFrame()
    r_last = len(df) - 1

    # 最終行が MarketSPEED 2 RSS のセパレータの場合はその行を削除する
    if df.iat[r_last, 0] == '--------':
        df = df.iloc[0:r_last].copy()

    # 日付列と時刻列の文字列を結合して Datetime 型へ変換してインデックスに設定
    df.index = pd.to_datetime(
        [
            '%s %s' % (
                df['日付'].iloc[r], df['時刻'].iloc[r]
            ) for r in range(len(df))
        ]
    )
    df.index.name = 'Datetime'

    # 必要な列名のみコピーする
    list_col_part = ['始値', '高値', '安値', '終値', '出来高', 'TREND', 'PSAR', 'Period', 'Diff']
    df_part = df[list_col_part].copy()

    # 列名を変更
    list_col_new = ['Open', 'High', 'Low', 'Close', 'Volume', 'TREND', 'PSAR', 'Period', 'Diff']
    df_part.columns = list_col_new

    return df_part


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


def get_tick(res: AppRes, target: dict) -> pd.DataFrame:
    """

    :param res:
    :param target:
    :return:
    """
    # tick データの読み込み
    file_tick = get_csv_tick_name(res, target)
    if os.path.isfile(file_tick):
        df = pd.read_csv(file_tick)
    else:
        return pd.DataFrame()

    # 時酷烈に日付情報を付加、文字列から日付フォーマットへ変更
    df.index = pd.to_datetime(
        [
            '%s %s' % (
                target['date_format'], df['Time'].iloc[r],
            ) for r in range(len(df))
        ]
    )
    df.index.name = 'Datetime'

    # 一旦 Series にコピーしてから DataFrame で返す
    ser = df['Price'].copy()
    ser.name = 'Price'
    return pd.DataFrame(ser)


def read_json(jsonfile: str) -> dict:
    """
    指定された JSON ファイルを読み込む
    :param jsonfile:
    :return:
    """
    with open(jsonfile) as f:
        dict_contents = json.load(f)
    return dict_contents
