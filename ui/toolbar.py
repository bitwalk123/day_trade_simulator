import os
import pandas as pd
import yfinance as yf

from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCalendarWidget,
    QToolBar,
    QToolButton, QComboBox,
)

from func.tide import get_dates
from widgets.dialogs import DialogWarning


class ToolBar(QToolBar):
    readDataFrame = Signal(pd.DataFrame)

    tickers = {
        '三菱ＵＦＪフィナンシャルＧ': '8306',
    }

    def __init__(self):
        super().__init__()
        self.calendar = None

        but_calendar = QToolButton()
        but_calendar.setIcon(QIcon('images/calendar.png'))
        but_calendar.clicked.connect(self.on_calendar_clicked)
        self.addWidget(but_calendar)

        self.combo_tickers = combo_tickers = QComboBox()
        combo_tickers.addItems(self.tickers.keys())
        self.addWidget(combo_tickers)

    def on_calendar_clicked(self):
        self.calendar = QCalendarWidget()
        self.calendar.setWindowTitle('データ取得日')
        self.calendar.activated.connect(self.on_date_selected)
        self.calendar.show()

    def on_date_selected(self, qdate: QDate):
        if self.calendar is not None:
            self.calendar.hide()
            self.calendar.deleteLater()

        # dt_today = dt.datetime.now()
        qdate_today = QDate.currentDate()
        if qdate_today <= qdate:
            msg_warning = '過去の日付を選択してください。'
            DialogWarning(msg_warning)
            return

        if qdate.daysTo(qdate_today) > 28:
            msg_warning = '日付が古すぎます。'
            DialogWarning(msg_warning)
            return

        str_year = '{:0=4}'.format(qdate.year())
        str_month = '{:0=2}'.format(qdate.month())
        str_day = '{:0=2}'.format(qdate.day())
        date_target = '%s-%s-%s' % (str_year, str_month, str_day)

        key = self.combo_tickers.currentText()
        code = self.tickers[key]

        csvfile = 'src/%s_%s.csv' % (code, date_target)
        if not os.path.isfile(csvfile):
            # Yahoo Finance から１分足データを取得
            start, end = get_dates(date_target)
            symbol = '%s.T' % code
            ticker = yf.Ticker(symbol)
            df = ticker.history(period='1d', interval='1m', start=start, end=end)
            if len(df) == 0:
                msg_warning = 'データを取得できませんでした。'
                DialogWarning(msg_warning)
                return

            # 時間情報のタイムゾーン部分を削除
            name_index = df.index.name
            df.index = [ts_jst.tz_localize(None) for ts_jst in df.index]
            df.index.name = name_index

            # 前場と後場の間に（なぜか）余分なデータが含まれているので削除
            date_str = str(df.index[0].date())
            dt_lunch_1 = pd.to_datetime('%s 11:30:00' % date_str)
            dt_lunch_2 = pd.to_datetime('%s 12:30:00' % date_str)
            df1 = df[df.index <= dt_lunch_1]
            df2 = df[df.index >= dt_lunch_2]
            df = pd.concat([df1, df2])

            # 取得したデータフレームを CSV 形式で保存
            df.to_csv(csvfile)
        else:
            df = pd.read_csv(csvfile, index_col=0)

        self.readDataFrame.emit(df)
