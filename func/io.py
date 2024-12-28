import json

import pandas as pd
import yfinance as yf

from func.tide import get_dates


def get_ohlc_1m(symbol: str, date_target: str) -> pd.DataFrame:
    """
    １分足データを取得
    :param symbol:
    :param date_target:
    :return:
    """
    ticker = yf.Ticker(symbol)
    start, end = get_dates(date_target)
    return ticker.history(
        period='1d',
        interval='1m',
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
