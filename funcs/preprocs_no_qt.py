import pandas as pd

list_col_part = [
    '始値', '高値', '安値', '終値', '出来高',
    'H_Open', 'H_High', 'H_Low', 'H_Close',
    'TREND', 'EP', 'AF', 'PSAR', 'Period', 'Diff', 'Slope', 'IQR'
]
list_col_part_en = [
    'Open', 'High', 'Low', 'Close', 'Volume',
    'H_Open', 'H_High', 'H_Low', 'H_Close',
    'TREND', 'EP', 'AF', 'PSAR', 'Period', 'Diff', 'Slope', 'IQR'
]


def get_ohlc4analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    VBAアプリの「OHLC1m」シートを CSV 形式で保存したファイルを読み込んでMatplotlibで利用しやすい形式に整形
    :param df:
    :return:
    """
    # 最後の行を除外
    df = df.iloc[:len(df) - 1]

    # インデックスを時刻情報に
    df.index = [pd.to_datetime(
        "%s %s:00" % (df.iloc[r]['日付'], df.iloc[r]['時刻'])
    ) for r in range(len(df))]

    # 必要な列だけ抽出
    df = df[list_col_part]

    # 列名を英語に
    df.columns = list_col_part_en

    return df
