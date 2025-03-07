import pandas as pd
import re

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


def get_date_formatted(dateStr: str) -> str:
    pattern = re.compile(r'^([0-9]{4})([0-9]{2})([0-9]{2})$')
    m = pattern.match(dateStr)
    if m:
        return '%s-%s-%s' % (
            m.group(1),
            m.group(2),
            m.group(3),
        )
    else:
        return '1970-01-01'


def get_ohlc4analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    VBAアプリの「OHLC1m」シートを CSV 形式で保存したファイルを読み込んでMatplotlibで利用しやすい形式に整形
    :param df:
    :return:
    """
    # 最後の行を除外
    df = df.iloc[1:len(df) - 1]

    # インデックスを時刻情報に
    df.index = [pd.to_datetime(
        "%s %s:00" % (df.iloc[r]['日付'], df.iloc[r]['時刻'])
    ) for r in range(len(df))]

    # 必要な列だけ抽出
    df = df[list_col_part]

    # 列名を英語に
    df.columns = list_col_part_en

    # 全列を数値として扱う
    for col in df.columns:
        df[col] = df[col].astype(float)

    return df


def get_tick4analysis(df: pd.DataFrame, dateFmt: str) -> pd.DataFrame:
    df.index = [pd.to_datetime(
        '%s %s' % (dateFmt, df.iat[r, 0])
    ) for r in range(len(df))]
    df.index.name = 'Datetime'
    df['Price'] = df['Price'].astype(float)

    return pd.DataFrame(df['Price'])
