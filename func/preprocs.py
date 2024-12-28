import pandas as pd


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
