import pandas as pd


def wilder_rsi(df: pd.DataFrame, colname: str = 'Price', period: int = 9) -> pd.Series:
    delta = df[colname].diff()

    price_up, price_down = delta.copy(), delta.copy()
    price_up[price_up < 0] = 0
    price_down[price_down > 0] = 0

    price_gain = price_up.ewm(com=(period - 1), min_periods=period).mean()
    price_loss = price_down.abs().ewm(com=(period - 1), min_periods=period).mean()

    rs = price_gain / price_loss
    return pd.Series(100 - (100 / (1 + rs)), name='RSI')
