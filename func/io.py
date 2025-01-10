import json
import os

import pandas as pd
import yfinance as yf

from func.common import get_csv_ohlc_name
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
    file_ohlc = get_csv_ohlc_name(res, target)
    df = pd.read_csv(file_ohlc, index_col=0)

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
