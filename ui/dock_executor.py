import os
import re

from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QDockWidget, QCheckBox, QPushButton, QWidget, QSizePolicy

from structs.res import AppRes
from widgets.checks import CheckBoxFile
from widgets.container import ScrollAreaVertical, Widget, PadH
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
        title = Widget()
        self.setTitleBarWidget(title)
        hbox = HBoxLayout()
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        title.setLayout(hbox)
        but_sell_all = QPushButton('Select All')
        but_sell_all.clicked.connect(self.select_all)
        hbox.addWidget(but_sell_all)
        but_desell_all = QPushButton('Deselect All')
        but_desell_all.clicked.connect(self.deselect_all)
        hbox.addWidget(but_desell_all)
        hpad = PadH()
        hbox.addWidget(hpad)

        # メイン
        sa = ScrollAreaVertical()
        self.setWidget(sa)

        base = Widget()
        base.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
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

    def cb_status_change_all(self, state: bool):
        for idx in range(self.vbox.count()):
            item = self.vbox.itemAt(idx)
            cb: QCheckBox | QWidget = item.widget()
            cb.setChecked(state)

    def deselect_all(self):
        self.cb_status_change_all(False)

    def select_all(self):
        state = True
        self.cb_status_change_all(True)

    def setExcelDir(self, dir: str):
        self.dir = dir
        files = sorted(os.listdir(dir))

        self.clear_layout()
        print(self.vbox.count())

        pattern = re.compile(r'^trader_[0-9]{8}\.xlsm$')
        for file in files:
            m = pattern.match(file)
            if m:
                cb = CheckBoxFile(file)
                self.vbox.addWidget(cb)
