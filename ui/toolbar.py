import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QToolBar

from structs.res import AppRes
from widgets.buttons import FolderToolButton
from widgets.dialog import FileDialogExcel


class ToolBar(QToolBar):
    fileSelected = Signal(str)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # ファイル選択用アイコン
        but_folder = FolderToolButton(res)
        but_folder.setToolTip('ファイル選択')
        but_folder.clicked.connect(self.on_file_dialog_open)
        self.addWidget(but_folder)

    def on_file_dialog_open(self):
        """
        Excel Macro ファイルの読み込み
        :return:
        """
        dialog = FileDialogExcel(self.res)
        # ファイルを選択されなければ何もしない
        if not dialog.exec():
            return

        # ----------------------------------
        # 🧿 選択されたファイルが存在して入れば通知
        # ----------------------------------
        file_excel = dialog.selectedFiles()[0]
        if os.path.isfile(file_excel):
            self.fileSelected.emit(file_excel)
