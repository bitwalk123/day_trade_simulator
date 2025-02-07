import os

import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QToolBar,
    QToolButton,
)

from structs.res import AppRes
from widgets.labels import LabelFlat


class ToolbarContour(QToolBar):
    provideFileName = Signal(str)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        # フォルダー用のアイコン
        but_folder = QToolButton()
        but_folder.setIcon(
            QIcon(os.path.join(self.res.dir_image, 'folder.png'))
        )
        but_folder.setToolTip('pickle ファイル選択')
        but_folder.clicked.connect(self.on_folder_clicked)
        self.addWidget(but_folder)

        self.addSeparator()

        self.lab_pkl = lab_pkl = LabelFlat('')
        self.addWidget(lab_pkl)

    def on_folder_clicked(self):
        dialog = QFileDialog()
        dialog.setNameFilters(['Picle files (*.pkl)'])
        dialog.setDirectory(self.res.dir_result)
        if not dialog.exec():
            return
        pklfile = dialog.selectedFiles()[0]
        self.lab_pkl.setText(os.path.basename(pklfile))
        self.provideFileName.emit(pklfile)
