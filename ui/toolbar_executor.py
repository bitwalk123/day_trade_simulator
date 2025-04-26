from PySide6.QtCore import Signal
from PySide6.QtWidgets import QToolBar

from structs.res import AppRes
from widgets.buttons import FolderButton
from widgets.dialog import DirDialog


class ToolbarExecutor(QToolBar):
    dirSelected = Signal(str)

    def __init__(self, res: AppRes):
        super().__init__()

        # =====================================================================
        #  UI
        # =====================================================================
        but_folder = FolderButton(res)
        but_folder.setToolTip('Excel ファイルが保存されているフォルダを選択')
        but_folder.clicked.connect(self.on_dlg_dir_sel)
        self.addWidget(but_folder)

    def on_dlg_dir_sel(self):
        dialog = DirDialog()
        if not dialog.exec():
            return

        basedir = dialog.selectedFiles()[0]
        self.dirSelected.emit(basedir)
