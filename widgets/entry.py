import os
import re

import pandas as pd
from PySide6.QtWidgets import QLineEdit, QSizePolicy


class Entry(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFrame(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(75)
        """
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred
        )
        """
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
        # self.setFixedWidth(300)
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
