import numpy as np
import pandas as pd


def get_tick_iqr(df: pd.DataFrame, date_str: str, past: int = 3) -> pd.Series:
    dict_columns = {
        't': [],
        'iqr': [],
    }
    df_iqr = pd.DataFrame.from_dict(dict_columns)
    df_iqr['t'] = df_iqr['t'].astype(object)
    df_iqr['iqr'] = df_iqr['iqr'].astype(float)

    td_step = pd.Timedelta(minutes=1)
    td_past = pd.Timedelta(minutes=past)

    dt_start_1 = pd.to_datetime('%s 9:03:00' % date_str)
    dt_end_1 = pd.to_datetime('%s 11:30:00' % date_str)

    dt_now = dt_start_1
    while dt_now <= dt_end_1:
        iqr = calc_tick_iqr(df, dt_now, td_past)
        append_row_iqr(df_iqr, dt_now - td_step, iqr)
        dt_now += td_step

    dt_start_2 = pd.to_datetime('%s 12:33:00' % date_str)
    dt_end_2 = pd.to_datetime('%s 15:24:00' % date_str)

    dt_now = dt_start_2
    while dt_now <= dt_end_2:
        iqr = calc_tick_iqr(df, dt_now, td_past)
        append_row_iqr(df_iqr, dt_now - td_step, iqr)
        dt_now += td_step

    df_iqr.index = pd.to_datetime(df_iqr['t'])
    df_iqr.index.name = 'Datetime'
    ser_iqr = df_iqr['iqr']

    return ser_iqr


def calc_tick_iqr(df, dt_now, td_past) -> float:
    df_part = df[(dt_now - td_past <= df.index) & (df.index < dt_now)]
    q75, q25 = np.percentile(df_part['Price'], [75, 25])

    return q75 - q25


def append_row_iqr(df, dt, iqr):
    r = len(df)
    df.at[r, 't'] = dt
    df.at[r, 'iqr'] = iqr
