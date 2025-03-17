import pandas as pd
import yfinance as yf
from PySide6.QtCore import QDate

from funcs.common import (
    get_excel_name,
    get_transaction_name,
)
from funcs.conv import df_to_html
from funcs.tide import (
    get_yyyy_mm_dd,
    get_yyyymmdd,
)
from structs.res import AppRes

# OHLCデータにおいて、オリジナルの列名とアプリで使用する列名
list_col_part = ['始値', '高値', '安値', '終値', '出来高', 'TREND', 'PSAR', 'Period', 'Diff', 'Slope', 'IQR']
list_col_new = ['Open', 'High', 'Low', 'Close', 'Volume', 'TREND', 'PSAR', 'Period', 'Diff', 'Slope', 'IQR']


def prep_dataset(file_excel: str) -> list:
    list_target = list()

    # ワークシート Cover の読み込み
    name_sheet_cover = 'Cover'
    df_cover = pd.read_excel(
        file_excel,
        sheet_name=name_sheet_cover,
        header=None,
        index_col=0,
    )

    # ワークシート Cover の列数
    n = len(df_cover.columns)
    # 銘柄毎にループ
    for c in range(n):
        dict_target = dict()

        # 銘柄コード
        r = list(df_cover.index).index('銘柄コード')
        code = df_cover.iloc[r, c]
        dict_target['code'] = code

        # Yahoo Finance から会社名を取得
        symbol = '%s.T' % code
        ticker = yf.Ticker(symbol)
        name = ticker.info['longName']
        dict_target['name'] = name

        # 現在日付の保持
        r = list(df_cover.index).index('現在日付')
        date = df_cover.iloc[r, c].replace('/', '-')
        dict_target['date'] = date

        # 呼び値
        r = list(df_cover.index).index('呼値')
        price_tick_min = df_cover.iloc[r, c]
        dict_target['price_tick_min'] = price_tick_min

        # AF
        r = list(df_cover.index).index('AF（初期値）')
        af_init = df_cover.iloc[r, c]
        dict_target['af_init'] = af_init

        r = list(df_cover.index).index('AF（ステップ）')
        af_step = df_cover.iloc[r, c]
        dict_target['af_step'] = af_step

        r = list(df_cover.index).index('AF（最大値）')
        af_max = df_cover.iloc[r, c]
        dict_target['af_max'] = af_max

        # 銘柄コードから、ティックデータ用ワークシート名を特定しティックデータを読み込む
        name_sheet_tick = 'tick_%s' % code
        df_tick = pd.read_excel(
            file_excel,
            sheet_name=name_sheet_tick,
            header=0,
        )
        # 時刻データを日付を含んだ Matplotlib で扱える形式に変換、インデックスへ
        df_tick.index = [pd.to_datetime('%s %s' % (date, t)) for t in df_tick['Time']]
        df_tick.index.name = 'Datetime'
        df_tick = df_tick[['Price', 'TREND', 'EP', 'AF', 'PSAR']]
        dict_target['tick'] = df_tick

        list_target.append(dict_target)

    return list_target


def prep_dataset_old(info: dict, qdate: QDate, res: AppRes) -> dict:
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

    # 取引履歴の保存
    save_transaction_history(dict_target, file_excel, res)

    # Tick データ準備
    prep_tick(dict_target, file_excel)

    # OHLC データ準備
    prep_ohlc(dict_target, file_excel, interval)

    return dict_target


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


def save_transaction_history(dict_target, file_excel, res):
    """
    取引履歴の保存
    :param dict_target:
    :param file_excel:
    :param res:
    :return:
    """
    # Excel から指定したワークシートのみ読み込む
    name_sheet_transaction = 'Transaction'
    df_transaction = pd.read_excel(file_excel, sheet_name=name_sheet_transaction)

    # 取引履歴のテーブルを HTML に変換
    list_col_format = ['int', 'str', 'str', 'int', 'int', 'int', 'int', 'str']
    list_html = df_to_html(df_transaction, list_col_format)

    # 所定のフォルダ仁保存
    file_transaction = get_transaction_name(res, dict_target)
    with open(file_transaction, mode='w') as f:
        f.writelines(list_html)

    # 時酷烈に日付情報を付加、文字列から日付フォーマットへ変更
    df_transaction = df_transaction.iloc[:len(df_transaction) - 1]
    df_transaction.index = pd.to_datetime(
        [
            '%s %s' % (
                dict_target['date_format'], df_transaction['時刻'].iloc[r],
            ) for r in range(len(df_transaction))
        ]
    )

    df_transaction.index.name = 'Datetime'
    dict_target['transaction'] = pd.DataFrame(df_transaction['売買'])


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
