import os

from funcs.io import get_doe_json
from structs.res import AppRes
from ui.panel_losscut import PanelLossCut
from ui.panel_output import PanelOutput
from ui.panel_param import PanelParam
from widgets.buttons import StartButton
from widgets.combo import ComboBox
from widgets.container import Widget, PadH
from widgets.dialog import DirDialog
from widgets.labels import LabelTitle, LabelDate, LabelFlat
from widgets.layouts import GridLayout


class PanelExecutor(Widget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        layout = GridLayout()
        self.setLayout(layout)

        col_max = 4
        r = 0
        labCode = LabelTitle('銘柄コード')
        layout.addWidget(labCode, r, 0)

        self.comboCode = comboCode = ComboBox()
        layout.addWidget(comboCode, r, 1)

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
        self.panelOutput = panel_output = PanelOutput(res)
        panel_output.selectDir.connect(self.on_dir_dialog_select)
        layout.addWidget(panel_output, r, 0, 1, col_max)

        r += 1
        self.btnStart = but_start = StartButton(res)
        but_start.setFixedHeight(40)
        but_start.setToolTip('シミュレーション開始')
        but_start.clicked.connect(self.on_simulation_start)
        layout.addWidget(but_start, r, 0, 1, col_max)

    def on_json_changed(self, file_json: str):
        self.panelParam.genTable(self.res, file_json)

    def on_dir_dialog_select(self):
        dialog = DirDialog()
        if not dialog.exec():
            return

        basedir = dialog.selectedFiles()[0]
        dateStr = self.objDate.text()
        if dateStr is not None:
            self.path_output = path = os.path.join(basedir, dateStr)
            self.panelOutput.setOutput(path)

    def on_simulation_start(self):
        pass