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

from func.io import get_ohlc_1m, read_json
from func.preprocs import reformat_dataframe
from func.tide import (
    get_time_breaks,
    get_yyyy_mm_dd,
    remove_tz_from_index,
)
from structs.res import AppRes
from widgets.dialogs import DialogWarning


class ToolBar(QToolBar):
    readDataFrame = Signal(pd.DataFrame)

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

        # 対象銘柄のコード（東証の銘柄に限る）
        key = self.combo_tickers.currentText()
        code = self.tickers[key]

        # CSV ファイル名の設定
        csvfile = os.path.join(
            self.res.dir_ohlc, '%s_%s.csv' % (code, date_target)
        )
        if os.path.isfile(csvfile):
            # すでに取得している CSV 形式の OHLC データをデータフレームへ読込
            df = pd.read_csv(csvfile, index_col=0)
        else:
            # １分足データを取得
            symbol = '%s.T' % code
            df = get_ohlc_1m(symbol, date_target)
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
            df = reformat_dataframe(df, dt_lunch_1, dt_lunch_2)

            # 取得したデータフレームを CSV 形式で保存
            df.to_csv(csvfile)

        # シグナル
        self.readDataFrame.emit(df)
