import os

from structs.res import AppRes


def get_csv_ohlc_name(res: AppRes, target: dict) -> str:
    return os.path.join(
        res.dir_ohlc, 'ohlc_%s_%s_%s.csv' % (
            target["interval"], target["code"], target["date"]
        )
    )

def get_csv_tick_name(res: AppRes, target: dict) -> str:
    return os.path.join(
        res.dir_tick, 'tick_%s_%s.csv' % (
            target["code"], target["date"]
        )
    )
