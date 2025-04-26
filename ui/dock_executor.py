import os
import re

from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QDockWidget, QCheckBox, QPushButton, QWidget

from structs.res import AppRes
from widgets.container import ScrollAreaVertical, Widget
from widgets.layouts import VBoxLayout, HBoxLayout


class DockExecutor(QDockWidget):

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        self.dir = None

        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # タイトルバー
        but_all = QPushButton('Select All')
        but_all.clicked.connect(self.select_all)
        self.setTitleBarWidget(but_all)

        # メイン
        sa = ScrollAreaVertical()
        self.setWidget(sa)

        base = Widget()
        sa.setWidget(base)

        self.vbox = vbox = VBoxLayout()
        base.setLayout(vbox)

    def clear_layout(self):
        while self.vbox.count():
            # 常に先頭を削除するようにループ
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def select_all(self):
        for idx in range(self.vbox.count()):
            item = self.vbox.itemAt(idx)
            cb: QCheckBox | QWidget = item.widget()
            cb.setChecked(True)

    def setExcelDir(self, dir: str):
        self.dir = dir
        files = sorted(os.listdir(dir))

        self.clear_layout()
        print(self.vbox.count())

        pattern = re.compile(r'^trader_[0-9]{8}\.xlsm$')
        for file in files:
            m = pattern.match(file)
            if m:
                cb = QCheckBox(file)
                self.vbox.addWidget(cb)
