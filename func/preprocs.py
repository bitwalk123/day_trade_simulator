import pandas as pd
from PySide6.QtCore import QDate

from func.io import get_ohlc, get_tick
from func.tide import get_yyyymmdd, get_yyyy_mm_dd
from structs.res import AppRes


def reformat_dataframe(df: pd.DataFrame, dt_lunch_1, dt_lunch_2) -> pd.DataFrame:
    """
    前場と後場の間に（なぜか）余分なデータが含まれているので削除
    :param df:
    :param dt_lunch_1:
    :param dt_lunch_2:
    :return:
    """
    df1 = df[df.index <= dt_lunch_1].copy()
    df2 = df[df.index >= dt_lunch_2].copy()
    return pd.concat([df1, df2])


def prepDataset(info: dict, qdate: QDate, res: AppRes) -> dict:
    """
    シミュレーション用のデータセット作成
    :param info:
    :param qdate:
    :param res:
    :return:
    """
    # QDate から文字列 YYYY-MM-DD を生成
    date_target = get_yyyymmdd(qdate)
    date_format_target = get_yyyy_mm_dd(qdate)

    # 扱うデータ情報
    interval = '1m'
    dict_target = {
        'code': info['code'],
        'date': date_target,
        'date_format': date_format_target,
        'name': info['name'],
        'symbol': info['symbol'],
        'price_delta_min': info['price_delta_min'],
        'unit': info['unit'],
    }

    # １分足データを取得
    df_ohlc = get_ohlc(res, dict_target, interval)
    dict_target[interval] = df_ohlc

    # ティックデータを取得
    df_tick = get_tick(res, dict_target)
    dict_target['tick'] = df_tick

    return dict_target
