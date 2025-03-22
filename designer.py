import sys
import pandas as pd
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QFileDialog

from structs.res import AppRes
from widgets.buttons import FolderButton, StartButton
from widgets.container import ScrollAreaVertical
from widgets.entry import Entry
from widgets.layouts import GridLayout


class Designer(QMainWindow):
    __app_name__ = 'Experiment Designer'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.threadpool = QThreadPool()

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

        ent_folder = Entry()
        ent_folder.setFixedWidth(200)
        layout.addWidget(ent_folder, r, 1)

        but_start = StartButton(res)
        layout.addWidget(but_start, r, 2)

    def on_file_dialog_open(self):
        """
        Excel Macro ファイルの読み込み
        :return:
        """
        dialog = QFileDialog()
        # 初期ディレクトリを指定
        dialog.setDirectory(self.res.dir_excel)
        # 拡張子のフィルターを設定
        dialog.setNameFilters(
            [
                'Excel Macro (*.xlsm)',
                'All files (*)',
            ]
        )
        # ファイルを選択されなければ何もしない
        if not dialog.exec():
            return

        file_excel = dialog.selectedFiles()[0]
        xl = pd.ExcelFile(file_excel)
        print(xl.sheet_names)


def main():
    app = QApplication(sys.argv)
    win = Designer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
