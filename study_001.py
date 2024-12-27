import pandas as pd
import yfinance as yf

from func.tide import get_dates

if __name__ == '__main__':
    date_target = '2024-12-26'

    start, end = get_dates(date_target)
    print(start, end)

    symbol = '8306.T'
    ticker = yf.Ticker(symbol)

    df = ticker.history(period='1d', interval='1m', start=start, end=end)
    print(df)

    name_index = df.index.name
    df.index = [ts_jst.tz_localize(None) for ts_jst in df.index]
    df.index.name = name_index
    print(df)

    date_str = str(df.index[0].date())
    dt_lunch_1 = pd.to_datetime('%s 11:30:00' % date_str)
    dt_lunch_2 = pd.to_datetime('%s 12:30:00' % date_str)

    df1 = df[df.index <= dt_lunch_1]
    df2 = df[df.index >= dt_lunch_2]
    df = pd.concat([df1, df2])
    print(df)
