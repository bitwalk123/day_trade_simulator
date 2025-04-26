import os
import re

import pandas as pd
from PySide6.QtCore import Signal, QMargins
from PySide6.QtWidgets import QLineEdit, QSizePolicy

from structs.res import AppRes
from widgets.buttons import FolderButton
from widgets.container import Widget, PadH
from widgets.layouts import HBoxLayout


class Entry(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFrame(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(75)
        self.setStyleSheet("""
            QLineEdit {
                font-family: monospace;
                background-color: white;
                color: black;
                padding-left:5px;
            }
        """)


class EntryDir(Entry):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(300)
        self.setEnabled(False)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )


class EntryExcelFile(Entry):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setEnabled(False)

        self.filename = None
        self.list_sheet = list()

        self.pattern = re.compile(r'tick_.*')

    def setExcelFile(self, filename: str):
        self.filename = filename
        self.setText(os.path.basename(filename))
        obj_excel = pd.ExcelFile(filename)
        self.list_sheet = list()
        for sheet in list(obj_excel.sheet_names):
            m = self.pattern.match(sheet)
            if m:
                self.list_sheet.append(sheet)

    def getSheetList(self) -> list:
        return self.list_sheet

    def get_ExcelFile(self) -> str:
        return self.filename


class EntryWithDir(Widget):
    selectDir = Signal()

    def __init__(self, res: AppRes):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        layout = HBoxLayout()
        self.setLayout(layout)

        self.entOutput = entOutput = EntryDir()
        layout.addWidget(entOutput)

        but_dir = FolderButton(res)
        but_dir.clicked.connect(self.on_dir_dialog_select)
        layout.addWidget(but_dir)

        padh = PadH()
        layout.addWidget(padh)

    def on_dir_dialog_select(self):
        """
        dialog = DirDialog()
        if not dialog.exec():
            return

        basedir = dialog.selectedFiles()[0]
        dateStr = self.objDate.text()
        if dateStr is not None:
            self.entOutput.setText(os.path.join(basedir, dateStr))
        """
        self.selectDir.emit()

    def setDir(self, dir: str):
        self.entOutput.setText(dir)
