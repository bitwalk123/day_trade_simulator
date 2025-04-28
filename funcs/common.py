import os

import pandas as pd

from structs.res import AppRes


def add_data_af(df_target: pd.DataFrame, df_tbl: pd.DataFrame, colname: str):
    if len(df_target) == 0:
        df_target['af_init'] = df_tbl['af_init']
        df_target['af_step'] = df_tbl['af_step']
        df_target['af_max'] = df_tbl['af_max']

    df_target[colname] = df_tbl['total']


def get_csv_ohlc_name(res: AppRes, dict_info: dict, interval: str) -> str:
    return os.path.join(
        res.dir_ohlc, 'ohlc_%s_%s_%s.csv' % (
            interval, dict_info["code"], dict_info["date"]
        )
    )


def get_csv_tick_name(res: AppRes, dict_info: dict) -> str:
    return os.path.join(
        res.dir_tick, 'tick_%s_%s.csv' % (
            dict_info["code"], dict_info["date"]
        )
    )


def get_excel_name(res: AppRes, dict_info: dict) -> str:
    return os.path.join(
        res.dir_excel, 'trader_%s_%s.xlsm' % (
            dict_info["code"], dict_info["date"]
        )
    )


def get_transaction_name(res: AppRes, dict_info: dict) -> str:
    return os.path.join(
        res.dir_transaction, 'transaction_%s_%s.html' % (
            dict_info["code"], dict_info["date"]
        )
    )
