import os

from structs.res import AppRes


def get_csv_name(res: AppRes, target: dict) -> str:
    return os.path.join(
        res.dir_ohlc, '%s_%s_%s.csv' % (
            target["code"], target["date"], target["interval"]
        )
    )
