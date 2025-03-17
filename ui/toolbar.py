import os

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QToolBar,
    QToolButton, QFileDialog,
)

from structs.res import AppRes


class ToolBar(QToolBar):
    fileSelected = Signal(str)
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # ファイル選択用アイコン
        but_folder = QToolButton()
        but_folder.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'folder.png'))
        )
        but_folder.setToolTip('ファイル選択')
        but_folder.clicked.connect(self.on_file_dialog_open)
        self.addWidget(but_folder)

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

        # 選択されたファイルが存在して入ればシグナル
        file_excel = dialog.selectedFiles()[0]
        if os.path.isfile(file_excel):
            self.fileSelected.emit(file_excel)