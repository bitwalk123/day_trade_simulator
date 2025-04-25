import os
import re

from PySide6.QtWidgets import QDockWidget, QWidget, QCheckBox

from structs.res import AppRes
from widgets.layouts import VBoxLayout


class DockExecutor(QDockWidget):

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        self.dir = None

        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        base = QWidget()
        self.setWidget(base)
        self.vbox = vbox = VBoxLayout()
        base.setLayout(vbox)

    def setExcelDir(self, dir: str):
        self.dir = dir
        files = sorted(os.listdir(dir))

        pattern = re.compile(r'^trader_.+\.xlsm$')
        for file in files:
            m = pattern.match(file)
            if m:
                self.vbox.addWidget(QCheckBox(file))
