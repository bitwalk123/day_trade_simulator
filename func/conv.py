import pandas as pd


def df_to_html(df: pd.DataFrame, list_col_format: list) -> list:
    list_html = list()
    list_html.append('<style>\n')
    list_html.append('table {border-collapse: collapse; font-family: monospace; font-size: small;}\n')
    list_html.append('th,td {border: solid 1px #aaa; padding: 0 5px;}\n')
    list_html.append('</style>\n')

    list_html.append('<table>\n')
    list_html.append('<thead>\n')
    list_html.append('<tr>\n')
    for colname in df.columns:
        list_html.append('<th>%s</th>\n' % colname)
    list_html.append('</tr>\n')
    list_html.append('</thead>\n')

    list_html.append('<tbody>\n')
    rows = len(df)
    cols = len(df.columns)
    for r in range(rows):
        list_html.append('<tr>\n')
        for c in range(cols):
            value = df.iat[r, c]
            if list_col_format[c] == 'str':
                list_html.append('<td>%s</td>\n' % value)
            elif list_col_format[c] == 'ts':
                if len(str(value)) > 0:
                    dt = pd.to_datetime(value)
                    str_hh = '{:0=2}'.format(dt.hour)
                    str_mm = '{:0=2}'.format(dt.minute)
                    str_ss = '{:0=2}'.format(dt.second)
                    list_html.append('<td>%s:%s:%s</td>\n' % (str_hh, str_mm, str_ss))
                else:
                    list_html.append('<td>%s</td>\n' % value)
            else:
                try:
                    list_html.append('<td style="text-align: right;">{:,}</td>\n'.format(int(value)))
                except ValueError:
                    list_html.append('<td>%s</td>\n' % value)

        list_html.append('</tr>\n')

    list_html.append('</tbody>\n')

    list_html.append('</table>\n')

    return list_html
