import os

from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCalendarWidget,
    QComboBox,
    QToolBar,
    QToolButton,
)

from funcs.io import (
    read_json,
)
from funcs.preprocs import prep_dataset
from structs.res import AppRes


class ToolBar(QToolBar):
    readyDataset = Signal(dict)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        # 銘柄リスト（辞書）の読み込み
        json_ticker = os.path.join(res.dir_config, 'ticker.json')
        self.tickers = read_json(json_ticker)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        self.calendar = QCalendarWidget()
        self.calendar.setWindowTitle('データ取得日')
        self.calendar.activated.connect(self.on_date_selected)

        # カレンダー表示用のアイコン
        but_calendar = QToolButton()
        but_calendar.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'calendar.png'))
        )
        but_calendar.setToolTip('日付選択')
        but_calendar.clicked.connect(self.on_calendar_clicked)
        self.addWidget(but_calendar)

        # 銘柄
        self.combo_tickers = combo_tickers = QComboBox()
        combo_tickers.addItems([key for key in self.tickers.keys()])
        combo_tickers.setToolTip('銘柄選択')
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

        key = self.combo_tickers.currentText()
        # key（銘柄の名前）をキーにして入れ子になっている辞書を取り出す。
        info = self.tickers[key]
        info['name'] = key
        dict_target = prep_dataset(info, qdate, self.res)

        # データフレーム準備完了シグナル
        self.readyDataset.emit(dict_target)
