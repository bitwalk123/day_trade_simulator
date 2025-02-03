import os

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolBar, QToolButton, QStyle

from structs.res import AppRes
from widgets.labels import LabelRight, LabelFlat


class ToolbarOverlayAnalysis(QToolBar):
    backClicked = Signal()
    playClicked = Signal()

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        but_back = QToolButton()
        but_back.setIcon(self.get_builtin_icon('SP_MediaSkipBackward'))
        but_back.setToolTip('最初に戻す')
        but_back.clicked.connect(self.on_back)
        self.addWidget(but_back)

        but_play = QToolButton()
        but_play.setIcon(self.get_builtin_icon('SP_MediaPlay'))
        but_play.setToolTip('個別に表示')
        but_play.clicked.connect(self.on_play)
        self.addWidget(but_play)

        self.addSeparator()

        # カウント／トータル
        self.lab_count = lab_count = LabelRight()
        lab_count.setToolTip('カウント／トータル')
        self.addWidget(lab_count)

        self.addSeparator()

        # トレンド開始時間
        self.lab_ts = lab_ts = LabelFlat('')
        lab_ts.setToolTip('トレンド開始時間')
        self.addWidget(lab_ts)

    def get_builtin_icon(self, name_short: str) -> QIcon:
        name_full = getattr(QStyle.StandardPixmap, name_short)
        return self.style().standardIcon(name_full)

    def on_back(self):
        self.backClicked.emit()

    def on_play(self):
        self.playClicked.emit()

    def setCount(self, countStr: str):
        self.lab_count.setText(countStr)

    def setTimeStamp(self, ts):
        self.lab_ts.setText(str(ts))
