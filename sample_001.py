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
