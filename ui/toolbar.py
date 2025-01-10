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

from func.io import read_json, get_ohlc
from func.tide import (
    get_yyyymmdd,
)
from structs.res import AppRes
from widgets.dialogs import DialogWarning


class ToolBar(QToolBar):
    readDataFrame = Signal(dict)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        json_ticker = os.path.join(res.dir_config, 'ticker.json')
        self.tickers = read_json(json_ticker)

        self.calendar = QCalendarWidget()
        self.calendar.setWindowTitle('データ取得日')
        self.calendar.activated.connect(self.on_date_selected)

        # カレンダー表示用のアイコン
        but_calendar = QToolButton()
        but_calendar.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'calendar.png'))
        )
        but_calendar.clicked.connect(self.on_calendar_clicked)
        self.addWidget(but_calendar)

        # 銘柄
        self.combo_tickers = combo_tickers = QComboBox()
        combo_tickers.addItems(self.tickers.keys())
        self.addWidget(combo_tickers)

    def on_calendar_clicked(self):
        """
        カレンダーボタンがクリックされたときの処理
        :return:
        """
        if self.calendar is not None:
            self.calendar.show()

    def on_date_selected(self, qdate: QDate):
        """
        カレンダーで日付が選択されたときの処理
        :param qdate:
        :return:
        """
        if self.calendar is not None:
            self.calendar.hide()

        # データフレームを確認する辞書
        dict_df = dict()

        # QDate から文字列 YYYY-MM-DD を生成
        date_target = get_yyyymmdd(qdate)

        # １分足データを取得
        key = self.combo_tickers.currentText()
        interval = '1m'
        target = {
            "code": self.tickers[key]["code"],
            "symbol": self.tickers[key]["symbol"],
            "date": date_target,
            "interval": interval,
        }
        df = get_ohlc(self.res, target)
        if len(df) == 0:
            return

        dict_df[interval] = df

        print(df)
        # データフレーム準備完了シグナル
        #self.readDataFrame.emit(dict_df)
