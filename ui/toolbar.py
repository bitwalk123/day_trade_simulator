import os

from PySide6.QtCore import QDate, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCalendarWidget,
    QComboBox,
    QToolBar,
    QToolButton,
)

from func.io import (
    get_ohlc,
    get_tick,
    read_json,
)
from func.tide import (
    get_yyyymmdd,
    get_yyyy_mm_dd,
)
from structs.res import AppRes


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
        combo_tickers.addItems([key for key in self.tickers.keys()])
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
        date_format_target = get_yyyy_mm_dd(qdate)

        # 扱うデータ情報
        key = self.combo_tickers.currentText()
        interval = '1m'
        dict_target = {
            'code': self.tickers[key]['code'],
            'date': date_target,
            'date_format': date_format_target,
            'name': key,
            'symbol': self.tickers[key]['symbol'],
            'tick_price': self.tickers[key]['tick_price'],
            'unit': self.tickers[key]['unit'],
        }

        # １分足データを取得
        df_ohlc = get_ohlc(self.res, dict_target, interval)
        if len(df_ohlc) == 0:
            return
        dict_target[interval] = df_ohlc
        # print(df_ohlc)

        # ティックデータを取得
        df_tick = get_tick(self.res, dict_target)
        dict_target['tick'] = df_tick

        # データフレーム準備完了シグナル
        self.readDataFrame.emit(dict_target)
