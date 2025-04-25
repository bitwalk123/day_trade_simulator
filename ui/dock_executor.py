import os
import re

from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QDockWidget, QCheckBox

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
        # title = Widget()
        # hbox = HBoxLayout()
        # title.setLayout(hbox)
        cb_all = QCheckBox('Select All')
        cb_all.setStyleSheet('margin-left: 10px;')
        # hbox.addWidget(cb_all)
        # self.setTitleBarWidget(title)
        self.setTitleBarWidget(cb_all)

        # メイン
        sa = ScrollAreaVertical()
        self.setWidget(sa)

        base = Widget()
        sa.setWidget(base)

        self.vbox = vbox = VBoxLayout()
        base.setLayout(vbox)

    def setExcelDir(self, dir: str):
        self.dir = dir
        files = sorted(os.listdir(dir))

        pattern = re.compile(r'^trader_[0-9]{8}\.xlsm$')
        for file in files:
            m = pattern.match(file)
            if m:
                self.vbox.addWidget(QCheckBox(file))
