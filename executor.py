import os
import sys
import pandas as pd
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)

from structs.res import AppRes
from widgets.buttons import FolderButton
from widgets.combo import ComboBox
from widgets.container import ScrollAreaVertical
from widgets.dialog import FileDialogExcel
from widgets.entry import EntryExcelFile
from widgets.layouts import GridLayout


class Executor(QMainWindow):
    __app_name__ = 'Executor'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

        icon = QIcon(os.path.join(res.dir_image, 'start.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)

        sa = ScrollAreaVertical()
        self.setCentralWidget(sa)

        base = QWidget()
        sa.setWidget(base)

        layout = GridLayout()
        base.setLayout(layout)

        r = 0
        but_folder = FolderButton(res)
        but_folder.clicked.connect(self.on_file_dialog_open)
        layout.addWidget(but_folder, r, 0)

        self.ent_sheet = ent_sheet = EntryExcelFile()
        ent_sheet.setFixedWidth(200)
        layout.addWidget(ent_sheet, r, 1)

        self.combo_sheet = combo_sheet = ComboBox()
        layout.addWidget(combo_sheet, r, 2)

    def on_file_dialog_open(self):
        """
        Excel Macro ファイルの読み込み
        :return:
        """
        dialog = FileDialogExcel(self.res)
        # ファイルを選択されなければ何もしない
        if not dialog.exec():
            return

        file_excel = dialog.selectedFiles()[0]
        self.ent_sheet.setExcelFile(file_excel)
        #xl = pd.ExcelFile(file_excel)
        self.combo_sheet.addItems(self.ent_sheet.getSheetList())


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
