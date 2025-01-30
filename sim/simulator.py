import datetime

import pandas as pd
from PySide6.QtCore import QObject, Signal


class Timer4Sim(QObject):
    updateSystemTime = Signal(str)
    updateTickPrice = Signal(str, float)

    def __init__(self):
        super().__init__()

    def start(self, dict_target: dict):
        df_tick = dict_target['tick']
        date_str = dict_target['date_format']
        t_current = t_start = pd.to_datetime('%s 09:00:00' % date_str)
        t_end = pd.to_datetime('%s 15:31:00' % date_str)
        t_delta = datetime.timedelta(seconds=1)

        while t_current <= t_end:
            t_formatted = t_current.strftime('%H:%M:%S')
            self.updateSystemTime.emit(t_formatted)

            if t_current in df_tick.index:
                p_current = df_tick.at[t_current, 'Price']
                self.updateTickPrice.emit(t_formatted, p_current)

            t_current += t_delta
