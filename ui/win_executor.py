import os

from PySide6.QtCore import Signal

from funcs.io import get_doe_json
from structs.res import AppRes
from ui.panel_losscut import PanelLossCut
from ui.panel_param import PanelParam
from widgets.buttons import StartButton
from widgets.combo import ComboBox
from widgets.container import Widget, PadH
from widgets.dialog import DirDialog
from widgets.entry import EntryFile, EntryWithDir
from widgets.labels import (
    LabelDate,
    LabelFlat,
    LabelString,
    LabelTitle,
)
from widgets.layouts import GridLayout


class WinExecutor(Widget):
    startClicked = Signal()

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        layout = GridLayout()
        self.setLayout(layout)

        col_max = 4

        r = 0
        labOutPath = LabelTitle('出力先')
        layout.addWidget(labOutPath, r, 0)

        self.output_dir = output_dir = EntryWithDir(res)
        output_dir.selectDir.connect(self.on_dir_dialog_select)
        layout.addWidget(output_dir, r, 1, 1, col_max - 1)

        r += 1
        labSrcFile = LabelTitle('ソース')
        layout.addWidget(labSrcFile, r, 0)

        self.entSrcFile = entSrcFile = EntryFile()
        layout.addWidget(entSrcFile, r, 1, 1, col_max - 1)

        r += 1
        labCode = LabelTitle('銘柄コード')
        layout.addWidget(labCode, r, 0)

        self.objCode = objCode = LabelString()
        layout.addWidget(objCode, r, 1)

        r += 1
        labDate = LabelTitle('現在日付')
        layout.addWidget(labDate, r, 0)

        self.objDate = objDate = LabelDate()
        layout.addWidget(objDate, r, 1)

        r += 1
        labLossCut = LabelTitle('ロスカット')
        layout.addWidget(labLossCut, r, 0)

        self.panelLossCut = panel_losscut = PanelLossCut(res)
        layout.addWidget(panel_losscut, r, 1, 1, col_max - 1)

        r += 1
        labLevel = LabelFlat('【水準】')
        layout.addWidget(labLevel, r, 0)

        self.objComboLevel = objComboLevel = ComboBox()
        list_json = get_doe_json(res)
        objComboLevel.addItems(list_json)
        objComboLevel.currentTextChanged.connect(self.on_json_changed)
        layout.addWidget(objComboLevel, r, 1, 1, 2)

        hpad = PadH()
        layout.addWidget(hpad, r, 3, 1, col_max - 3)

        r += 1
        file_json = objComboLevel.currentText()
        self.panelParam = panel_param = PanelParam(res, file_json)
        layout.addWidget(panel_param, r, 0, 1, col_max)

        r += 1
        self.btnStart = but_start = StartButton(res)
        but_start.setFixedHeight(40)
        but_start.setToolTip('シミュレーション開始')
        but_start.clicked.connect(self.on_simulation_start)
        layout.addWidget(but_start, r, 0, 1, col_max)

    def getLevelMax(self) -> int:
        return self.panelParam.getLevelMax()

    def getOutputDir(self) -> str:
        return self.output_dir.getDir()

    def on_json_changed(self, file_json: str):
        self.panelParam.genTable(self.res, file_json)

    def on_dir_dialog_select(self):
        dialog = DirDialog()
        if not dialog.exec():
            return

        dir_output = dialog.selectedFiles()[0]
        self.output_dir.setDir(dir_output)

    def on_simulation_start(self):
        self.startClicked.emit()

    def setCode(self, code: str):
        self.objCode.setText(code)

    def setDate(self, date: str):
        self.objDate.setText(date)

    def setSrcFile(self, file: str):
        self.entSrcFile.setText(file)
