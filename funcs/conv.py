import datetime

import numpy as np
import pandas as pd

from funcs.tide import get_time_str


def df_to_html(df: pd.DataFrame, list_col_format: list, total_profit: float) -> list:
    """

    :param df:
    :param list_col_format:
        ex. list_col_format = ['int', 'ts', 'str', 'int', 'int', 'int', 'int', 'str']
    :return:
    """
    list_html = list()

    # style
    list_html.append('<style>\n')
    list_html.append(
        'table {border-collapse: collapse; border: solid 1px #aaa; font-family: monospace; font-size: x-small;}\n')
    list_html.append('th,td {border-bottom: solid 1px #aaa; padding: 0 5px;}\n')
    list_html.append('</style>\n')

    # table
    list_html.append('<table>\n')

    # header
    list_html.append('<thead>\n')
    list_html.append('<tr>\n')
    for colname in df.columns:
        list_html.append('<th nowrap>%s</th>\n' % colname)
    list_html.append('</tr>\n')
    list_html.append('</thead>\n')

    # body
    list_html.append('<tbody>\n')
    rows = len(df)
    cols = len(df.columns)
    for r in range(rows):
        list_html.append('<tr>\n')

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # table cells
        for c in range(cols):
            value = df.iat[r, c]
            if type(value) is int or type(value) is float or type(value) is np.float64:
                if np.isnan(value):
                    value = ''

            if list_col_format[c] == 'str':
                # _____________________________________________________________
                # string
                list_html.append('<td nowrap>%s</td>\n' % value)
            elif list_col_format[c] == 'ts':
                # _____________________________________________________________
                # datetime
                if len(str(value)) > 0:
                    dt = pd.to_datetime(value)
                    # extract only hh:mm:ss
                    hh = '{:0=2}'.format(dt.hour)
                    mm = '{:0=2}'.format(dt.minute)
                    ss = '{:0=2}'.format(dt.second)
                    list_html.append('<td nowrap>%s:%s:%s</td>\n' % (hh, mm, ss))
                else:
                    # '' may exist as blank
                    list_html.append('<td>%s</td>\n' % value)
            else:
                # _____________________________________________________________
                # numeric, treated as integer
                try:
                    list_html.append('<td nowrap style="text-align: right;">{:,}</td>\n'.format(int(value)))
                except ValueError:
                    list_html.append('<td nowrap>%s</td>\n' % value)

        list_html.append('</tr>\n')
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

    list_html.append('<tr>\n')
    list_html.append('<td colspan="4" style="text-align: right;">実現損益</td>\n')
    list_html.append('<td nowrap style="text-align: right;">{:,}</td>\n'.format(int(total_profit)))
    list_html.append('</tr>\n')

    list_html.append('</tbody>\n')

    # end of table
    list_html.append('</table>\n')

    return list_html


def get_formatted_tick_data(df: pd.DataFrame, date_str: str, colname: str) -> pd.DataFrame:
    """
    RssMarket 関数で取得した Tick データを秒単位のデータで整形する
    １分間に数個しかないデータ、たくさんあるデータそれぞれに対応して、１分間に等間隔に振り分ける。
    間隔はマイクロ秒単位で刻んで、秒単位に間引きする。
    :param df:
    :param date_str:
    :param colname:
    :return:
    """
    total = 60 * 1000000  # １秒間をマイクロ秒単位で扱う

    td1 = datetime.timedelta(microseconds=1)
    td2 = datetime.timedelta(seconds=1)

    df0 = df[df[colname] != '--------'].copy()
    list_time = sorted(list(set(df0[colname])))
    for time in list_time:
        ticktime = pd.to_datetime('%s %s' % (date_str, time))
        df1 = df0[df0[colname] == time]
        n = len(df1) # 行数 = 同時刻の個数
        if n > 0:
            step = int(total / n)  # １分間（マイクロ秒）を同時刻の個数で割ってステップ幅を決める
            for r in df1.index:
                df0.loc[r, 'Time'] = ticktime
                ticktime += td1 * step  # ステップ幅でインクリメント

    # 1 秒間隔のデータにフォーマット
    df_result = pd.DataFrame()
    dt = pd.to_datetime('%s %s' % (date_str, list_time[0]))
    dt_end = pd.to_datetime('%s 15:24:59' % date_str)
    while dt < dt_end:
        # 時刻は先頭 + 1 秒から始める。
        dt_target = dt + td2
        # 対象データは dt_target の 1 秒前から dt_target 直前まで
        df1 = df0[(dt <= df0['Time']) & (df0['Time'] < dt_target)]
        if len(df1) > 0:
            df_result.at[dt_target, 'Time'] = get_time_str(dt_target)
            # 株価は dt_target 直線の値を採用する
            df_result.at[dt_target, 'Price'] = df1['終値'].iloc[len(df1) - 1]
        dt = dt_target

    # 大引けの値があれば加えておく
    dt_target = pd.to_datetime('%s 15:30:00.0' % date_str)
    if dt_target == df0['Time'].iloc[len(df0) - 1]:
        df_result.at[dt_target, 'Time'] = get_time_str(dt_target)
        df_result.at[dt_target, 'Price'] = df0['終値'].iloc[len(df0) - 1]

    return df_result

def get_format_tick_sheet(df: pd.DataFrame, date_str: str, colname: str) -> pd.DataFrame:
    """
    RssMarket 関数で取得した Tick データを秒単位のデータで整形する
    １分間に数個しかないデータ、たくさんあるデータそれぞれに対応して、１分間に等間隔に振り分ける。
    間隔はマイクロ秒単位で刻んで、秒単位に間引きする。
    :param df:
    :param date_str:
    :param colname:
    :return:
    """
    total = 60 * 1000000  # １秒間をマイクロ秒単位で扱う

    td1 = datetime.timedelta(microseconds=1)
    td2 = datetime.timedelta(seconds=1)

    df0 = df[df[colname] != '--------'].copy()
    list_time = sorted(list(set(df0[colname])))
    for time in list_time:
        ticktime = pd.to_datetime('%s %s' % (date_str, time))
        df1 = df0[df0[colname] == time]
        n = len(df1) # 行数 = 同時刻の個数
        if n > 0:
            step = int(total / n)  # １分間（マイクロ秒）を同時刻の個数で割ってステップ幅を決める
            for r in df1.index:
                df0.loc[r, 'Time'] = ticktime
                ticktime += td1 * step  # ステップ幅でインクリメント

    # 1 秒間隔のデータにフォーマット
    df_result = pd.DataFrame()
    dt = pd.to_datetime('%s %s' % (date_str, list_time[0]))
    dt_end = pd.to_datetime('%s 15:24:59' % date_str)
    while dt < dt_end:
        # 時刻は先頭 + 1 秒から始める。
        dt_target = dt + td2
        # 対象データは dt_target の 1 秒前から dt_target 直前まで
        df1 = df0[(dt <= df0['Time']) & (df0['Time'] < dt_target)]
        if len(df1) > 0:
            df_result.at[dt_target, 'Time'] = get_time_str(dt_target)
            # 株価は dt_target 直線の値を採用する
            df_result.at[dt_target, 'Price'] = df1['終値'].iloc[len(df1) - 1]
        dt = dt_target

    # 大引けの値があれば加えておく
    dt_target = pd.to_datetime('%s 15:30:00.0' % date_str)
    if dt_target == df0['Time'].iloc[len(df0) - 1]:
        df_result.at[dt_target, 'Time'] = get_time_str(dt_target)
        df_result.at[dt_target, 'Price'] = df0['終値'].iloc[len(df0) - 1]

    return df_result
