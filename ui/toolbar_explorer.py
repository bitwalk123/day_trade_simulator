import os

from PySide6.QtCore import Signal, QDate
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QStyle,
    QToolBar,
    QToolButton, QCalendarWidget,
)

from structs.res import AppRes


class ToolbarExplorer(QToolBar):
    playClicked = Signal()
    qdateSelected = Signal(QDate)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

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

        def on_date_selected(self, qdate: QDate):
            """
            カレンダーで日付が選択されたときの処理
            :param qdate:
            :return:
            """
            if self.calendar is not None:
                self.calendar.hide()

        but_play = QToolButton()
        but_play.setIcon(self.get_builtin_icon('SP_MediaPlay'))
        but_play.setToolTip('開始')
        but_play.clicked.connect(self.on_play)
        self.addWidget(but_play)

    def get_builtin_icon(self, name_short: str) -> QIcon:
        name_full = getattr(QStyle.StandardPixmap, name_short)
        return self.style().standardIcon(name_full)

    def on_play(self):
        self.playClicked.emit()

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
            self.qdateSelected.emit(qdate)
