import pandas as pd
import yfinance as yf

from func.tide import get_dates


def get_ohlc_1m(code: str, date_target: str) -> pd.DataFrame:
    """
    １分足データを取得
    :param code:
    :param date_target:
    :return:
    """
    symbol = '%s.T' % code
    ticker = yf.Ticker(symbol)

    start, end = get_dates(date_target)
    df = ticker.history(
        period='1d',
        interval='1m',
        start=start,
        end=end,
    )

    return df
