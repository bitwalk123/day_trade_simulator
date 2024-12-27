import os
import pandas as pd

from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCalendarWidget,
    QComboBox,
    QToolBar,
    QToolButton,
)

from func.io import get_ohlc_1m
from func.tide import get_yyyy_mm_dd, remove_tz_from_index, get_time_breaks
from widgets.dialogs import DialogWarning


class ToolBar(QToolBar):
    readDataFrame = Signal(pd.DataFrame)

    tickers = {
        '三菱ＵＦＪフィナンシャルＧ': '8306',
    }

    def __init__(self):
        super().__init__()
        self.calendar = QCalendarWidget()
        self.calendar.setWindowTitle('データ取得日')
        self.calendar.activated.connect(self.on_date_selected)

        but_calendar = QToolButton()
        but_calendar.setIcon(QIcon('images/calendar.png'))
        but_calendar.clicked.connect(self.on_calendar_clicked)
        self.addWidget(but_calendar)

        self.combo_tickers = combo_tickers = QComboBox()
        combo_tickers.addItems(self.tickers.keys())
        self.addWidget(combo_tickers)

    def on_calendar_clicked(self):
        if self.calendar is not None:
            self.calendar.show()

    def on_date_selected(self, qdate: QDate):
        if self.calendar is not None:
            self.calendar.hide()

        # dt_today = dt.datetime.now()
        qdate_today = QDate.currentDate()
        if qdate_today < qdate:
            msg_warning = '過去の日付を選択してください。'
            DialogWarning(msg_warning)
            return

        if qdate.daysTo(qdate_today) > 28:
            msg_warning = '日付が古すぎます。'
            DialogWarning(msg_warning)
            return

        # QDate から文字列 YYYY-MM-DD を生成
        date_target = get_yyyy_mm_dd(qdate)

        # 対象銘柄のコード
        key = self.combo_tickers.currentText()
        code = self.tickers[key]

        csvfile = 'src/%s_%s.csv' % (code, date_target)
        if not os.path.isfile(csvfile):
            # １分足データを取得
            df = get_ohlc_1m(code, date_target)
            if len(df) == 0:
                msg_warning = 'データを取得できませんでした。'
                DialogWarning(msg_warning)
                return

            # 時間情報のタイムゾーン部分を削除
            remove_tz_from_index(df)

            # 判定に使用する（日付付きの）時刻を取得
            dt_lunch_1, dt_lunch_2, dt_pre_ca = get_time_breaks(df)

            # 取得したデータが完全か確認
            if max(df.index) < dt_pre_ca:
                msg_warning = '取得したデータが不完全です。'
                DialogWarning(msg_warning)
                return

            # 前場と後場の間に（なぜか）余分なデータが含まれているので削除
            df1 = df[df.index <= dt_lunch_1]
            df2 = df[df.index >= dt_lunch_2]
            df = pd.concat([df1, df2])

            # 取得したデータフレームを CSV 形式で保存
            df.to_csv(csvfile)
        else:
            df = pd.read_csv(csvfile, index_col=0)

        # シグナル
        self.readDataFrame.emit(df)
