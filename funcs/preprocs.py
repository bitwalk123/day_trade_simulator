import pandas as pd
from PySide6.QtCore import QDate

from funcs.common import get_excel_name
from funcs.tide import get_yyyymmdd, get_yyyy_mm_dd
from structs.res import AppRes

# OHLCデータにおいて、オリジナルの列名とアプリで使用する列名
list_col_part = ['始値', '高値', '安値', '終値', '出来高', 'TREND', 'PSAR', 'Period', 'Diff', 'Slope', 'IQR']
list_col_new = ['Open', 'High', 'Low', 'Close', 'Volume', 'TREND', 'PSAR', 'Period', 'Diff', 'Slope', 'IQR']


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

    # Excel ファイル
    file_excel = get_excel_name(res, dict_target)

    # Tick データ準備
    prep_tick(dict_target, file_excel)

    # OHLC データ準備
    prep_ohlc(dict_target, file_excel, interval)

    return dict_target


def prep_ohlc(dict_target, file_excel, interval):
    # Excel から指定したワークシートのみ読み込む
    name_sheet_ohlc = 'OHLC%s' % interval
    df_ohlc = pd.read_excel(file_excel, sheet_name=name_sheet_ohlc)

    # 最終行が MarketSPEED 2 RSS のセパレータの場合はその行を削除する
    r_last = len(df_ohlc) - 1
    if df_ohlc.iat[r_last, 0] == '--------':
        df_ohlc = df_ohlc.iloc[0:r_last].copy()

    # 日付列と時刻列の文字列を結合して Datetime 型へ変換してインデックスに設定
    df_ohlc.index = pd.to_datetime(
        [
            '%s %s' % (
                df_ohlc['日付'].iloc[r], df_ohlc['時刻'].iloc[r]
            ) for r in range(len(df_ohlc))
        ]
    )
    df_ohlc.index.name = 'Datetime'

    # 必要な列名のみコピーする
    df_ohlc_part = df_ohlc[list_col_part].copy()
    df_ohlc_part.columns = list_col_new  # 列名を変更
    dict_target[interval] = df_ohlc_part


def prep_tick(dict_target, file_excel):
    # Excel から指定したワークシートのみ読み込む
    name_sheet_tick = 'Tick'
    df_tick = pd.read_excel(file_excel, sheet_name=name_sheet_tick)

    # 時酷烈に日付情報を付加、文字列から日付フォーマットへ変更
    df_tick.index = pd.to_datetime(
        [
            '%s %s' % (
                dict_target['date_format'], df_tick['Time'].iloc[r],
            ) for r in range(len(df_tick))
        ]
    )
    df_tick.index.name = 'Datetime'

    # 一旦 Series にコピーしてから DataFrame で返す
    ser_tick = df_tick['Price'].copy()
    ser_tick.name = 'Price'
    dict_target['tick'] = pd.DataFrame(ser_tick)


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
