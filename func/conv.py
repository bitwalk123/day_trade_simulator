import numpy as np
import pandas as pd


def df_to_html(df: pd.DataFrame, list_col_format: list) -> list:
    """

    :param df:
    :param list_col_format:
        ex. list_col_format = ['int', 'ts', 'str', 'int', 'int', 'int', 'int', 'str']
    :return:
    """
    list_html = list()

    # style
    list_html.append('<style>\n')
    list_html.append('table {border-collapse: collapse; border: solid 1px #aaa; font-family: monospace; font-size: x-small;}\n')
    list_html.append('th,td {border-bottom: solid 1px #aaa; padding: 0 5px;}\n')
    list_html.append('</style>\n')

    # table
    list_html.append('<table>\n')

    # header
    list_html.append('<thead>\n')
    list_html.append('<tr>\n')
    for colname in df.columns:
        list_html.append('<th>%s</th>\n' % colname)
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

    list_html.append('</tbody>\n')

    # end of table
    list_html.append('</table>\n')

    return list_html
