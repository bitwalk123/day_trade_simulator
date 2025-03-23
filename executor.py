import os
import sys
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget, QProgressBar,
)

from structs.res import AppRes
from widgets.buttons import ChooseButton, FolderButton
from widgets.combo import ComboBox
from widgets.container import ScrollAreaVertical
from widgets.dialog import FileDialogExcel
from widgets.entry import EntryExcelFile
from widgets.layouts import GridLayout
from widgets.statusbar import StatusBar
from widgets.toolbar import ToolBar


class Executor(QMainWindow):
    __app_name__ = 'Executor'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

        icon = QIcon(os.path.join(res.dir_image, 'start.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)

        toolbar = ToolBar()
        self.addToolBar(toolbar)

        but_folder = FolderButton(res)
        but_folder.clicked.connect(self.on_file_dialog_open)
        toolbar.addWidget(but_folder)

        self.ent_sheet = ent_sheet = EntryExcelFile()
        ent_sheet.setFixedWidth(200)
        toolbar.addWidget(ent_sheet)

        self.combo_sheet = combo_sheet = ComboBox()
        toolbar.addWidget(combo_sheet)

        self.but_choose = but_choose = ChooseButton(res)
        but_choose.setDisabled(True)
        toolbar.addWidget(but_choose)

        sa = ScrollAreaVertical()
        self.setCentralWidget(sa)

        base = QWidget()
        sa.setWidget(base)

        layout = GridLayout()
        base.setLayout(layout)

        statusbar = StatusBar()
        self.setStatusBar(statusbar)

        self.pbar = pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        statusbar.addPermanentWidget(pbar, stretch=1)

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
        self.combo_sheet.addItems(self.ent_sheet.getSheetList())
        self.but_choose.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    win = Executor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
