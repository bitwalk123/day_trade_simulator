import json
import os

import pandas as pd
import yfinance as yf

from func.common import get_csv_name
from func.preprocs import reformat_dataframe

from func.tide import (
    get_dates,
    get_time_breaks,
    remove_tz_from_index,
)
from structs.res import AppRes
from widgets.dialogs import DialogWarning


def get_ohlc(res: AppRes, target: dict) -> pd.DataFrame:
    """
    OHLC データをデータフレームで取得
    :param res:
    :param target:
    :return:
    """
    # OHLCのファイル名（CSV形式）
    file_ohlc = get_csv_name(res, target)

    if os.path.isfile(file_ohlc):
        # すでに取得している CSV 形式の OHLC データをデータフレームへ読込
        df = pd.read_csv(file_ohlc, index_col=0)
    else:
        # OHLC データを Yahoo Finance から取得
        df = get_ohlc_from_yahoo(target)
        if len(df) == 0:
            msg = 'データを取得できませんでした。'
            DialogWarning(msg)
            return pd.DataFrame()

        # 時間情報のタイムゾーン部分を削除
        remove_tz_from_index(df)

        # 判定に使用する（日付付きの）時刻を取得
        dt_lunch_1, dt_lunch_2, dt_pre_ca = get_time_breaks(df)

        # 取得したデータが完全か確認
        if max(df.index) < dt_pre_ca:
            msg = '取得したデータが不完全です。'
            DialogWarning(msg)
            return pd.DataFrame()

        # 前場と後場の間に（なぜか）余分なデータが含まれているので削除
        df = reformat_dataframe(df, dt_lunch_1, dt_lunch_2)

        # 取得したデータフレームを CSV 形式で保存
        df.to_csv(file_ohlc)

    # データフレームのインデックスを時関係式に設定
    name_index = df.index.name
    df.index = pd.to_datetime(df.index)
    df.index.name = name_index

    return df


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
