from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QStyle,
    QToolBar,
    QToolButton,
)

from structs.res import AppRes


class ToolbarExplorer(QToolBar):
    playClicked = Signal()

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

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
