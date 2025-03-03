import pandas as pd
from PySide6.QtCore import QDate

from funcs.common import get_excel_name, get_csv_ohlc_name, get_csv_tick_name
from funcs.io import get_ohlc, get_tick
from funcs.tide import get_yyyymmdd, get_yyyy_mm_dd
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


def prep_dataset(info: dict, qdate: QDate, res: AppRes) -> dict:
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

    # Excel ファイルから、必要データを一旦 CSV ファイルに保存する
    prep_excel(res, dict_target, interval)

    # １分足データを取得
    df_ohlc = get_ohlc(res, dict_target, interval)
    dict_target[interval] = df_ohlc

    # ティックデータを取得
    df_tick = get_tick(res, dict_target)
    dict_target['tick'] = df_tick

    return dict_target


def prep_excel(res: AppRes, dict_target: dict, interval: str):
    """
    Excel ファイルから、必要データを一旦 CSV ファイルに保存する
    :param res:
    :param dict_target:
    :param interval:
    :return:
    """

    # Excel ファイル
    file_excel = get_excel_name(res, dict_target)

    # Tick データ
    name_sheet_tick = 'Tick'
    df_tick = pd.read_excel(file_excel, sheet_name=name_sheet_tick)
    # dict_target['tick'] = df_tick
    file_csv_tick = get_csv_tick_name(res, dict_target)
    df_tick.to_csv(file_csv_tick, index=False)

    # OHLC データ
    name_sheet_ohlc = 'OHLC%s' % interval
    df_ohlc = pd.read_excel(file_excel, sheet_name=name_sheet_ohlc)
    # dict_target[interval] = df_ohlc
    file_csv_ohlc = get_csv_ohlc_name(res, dict_target, interval)
    df_ohlc.to_csv(file_csv_ohlc, index=False)


def prep_result_df(params: dict) -> pd.DataFrame:
    dict_result = {
        'code': list(),
        'date': list(),
    }
    for key in params.keys():
        dict_result[key] = list()
    dict_result['total'] = list()
    df = pd.DataFrame.from_dict(dict_result)
    df_result = df.astype(object)
    return df_result


def prep_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """
    読み込んだ OHLC ファイルを
    アプリが使用できる OHLC のデータフレームに整形
    :param df:
    :return:
    """
    # 一行目は前日のデータなので除く、
    # また最終行はセパレータ文字なのでこれも除く
    rows = len(df)
    df = df.iloc[1:(rows - 1)].reset_index(drop=True)

    # 必要な列のみ残す
    df = df[
        [
            # Market SPEED RSS からのデータ列
            '日付', '時刻', '始値', '高値', '安値', '終値', '出来高',
            # 平均足のデータ列
            'H_Open', 'H_High', 'H_Low', 'H_Close',
            # Parabolic SAR のデータ列
            'TREND', 'EP', 'AF', 'PSAR', 'Period', 'Diff', 'Slope',
            # IQR
            'IQR',
        ]
    ]

    # データフレームのインデックスを、「日付時刻」形式に変換
    df.index = [
        pd.to_datetime(
            '%s %s:00' % (d, t)
        ) for d, t in zip(df['日付'], df['時刻'])
    ]
    df.index.name = 'Datetime'

    # 日付、時刻列を除く
    df = df[
        [
            '始値', '高値', '安値', '終値', '出来高',
            'H_Open', 'H_High', 'H_Low', 'H_Close',
            'TREND', 'EP', 'AF', 'PSAR', 'Period', 'Diff', 'Slope',
            'IQR',
        ]
    ]

    # 列名を英名に揃える
    df.columns = [
        'Open', 'High', 'Low', 'Close', 'Volume',
        'H_Open', 'H_High', 'H_Low', 'H_Close',
        'TREND', 'EP', 'AF', 'PSAR', 'Period', 'Diff',
        'IQR',
    ]
    df = df.astype(float)

    return df.copy()


def prep_tick(df: pd.DataFrame, dateStr: str) -> pd.DataFrame:
    """
    読み込んだ Tick ファイルを
    アプリが使用できる Tick のデータフレームに整形

    :param df:
    :param dateStr:
    :return:
    """
    # データフレームのインデックスを、「日付時刻」形式に変換
    df.index = [
        pd.to_datetime(
            '%s %s' % (dateStr, t)
        ) for t in df['Time']
    ]
    df.index.name = 'Datetime'

    return pd.DataFrame(df['Price'].copy())
