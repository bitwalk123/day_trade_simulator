import os

from structs.res import AppRes


def get_csv_ohlc_name(res: AppRes, dict_info: dict) -> str:
    return os.path.join(
        res.dir_ohlc, 'ohlc_%s_%s_%s.csv' % (
            dict_info["interval"], dict_info["code"], dict_info["date"]
        )
    )

def get_csv_tick_name(res: AppRes, dict_info: dict) -> str:
    return os.path.join(
        res.dir_tick, 'tick_%s_%s.csv' % (
            dict_info["code"], dict_info["date"]
        )
    )
