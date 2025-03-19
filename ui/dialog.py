import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QMessageBox,
    QVBoxLayout,
)

from structs.res import AppRes
from widgets.frame import Frame
from widgets.labels import (
    LabelFlat,
    LabelTitleLeft,
)
from widgets.spinbox import DoubleSpinBox


def DialogWarning(message: str):
    dlg = QMessageBox()
    dlg.setWindowTitle('警告')
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setIcon(QMessageBox.Icon.Warning)
    dlg.exec()


class DlgAFSetting(QDialog):
    """
    Parabolic SAR の AF（加速因数）用の設定ダイアログ
    """

    def __init__(self, res: AppRes, dict_af: dict):
        super().__init__()
        self.dict_af = dict_af

        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('AF（加速因数）の設定')

        layout_base = QVBoxLayout()
        self.setLayout(layout_base)

        base = Frame()
        layout_base.addWidget(base)

        layout = QGridLayout()
        layout.setSpacing(0)
        base.setLayout(layout)

        r = 0
        labParameter = LabelFlat('Parabolic SAR')
        layout.addWidget(labParameter, r, 0)

        r += 1
        labAFinit = LabelTitleLeft('AF（初期値）')
        layout.addWidget(labAFinit, r, 0)

        self.objAFinit = objAFinit = DoubleSpinBox()
        objAFinit.setValue(self.dict_af['af_init'])
        layout.addWidget(objAFinit, r, 1)

        r += 1
        labAFstep = LabelTitleLeft('AF（ステップ）')
        layout.addWidget(labAFstep, r, 0)

        self.objAFstep = objAFstep = DoubleSpinBox()
        objAFstep.setValue(self.dict_af['af_step'])
        layout.addWidget(objAFstep, r, 1)

        r += 1
        labAFmax = LabelTitleLeft('AF（最大値）')
        layout.addWidget(labAFmax, r, 0)

        self.objAFmax = objAFmax = DoubleSpinBox()
        objAFmax.setValue(self.dict_af['af_max'])
        layout.addWidget(objAFmax, r, 1)

        dlgbtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        bbox = QDialogButtonBox(dlgbtn)
        bbox.accepted.connect(self.clickedAcceptButton)
        bbox.rejected.connect(self.clickedRejectButton)
        layout_base.addWidget(bbox)

    def clickedAcceptButton(self):
        self.dict_af['af_init'] = self.objAFinit.value()
        self.dict_af['af_step'] = self.objAFstep.value()
        self.dict_af['af_max'] = self.objAFmax.value()
        self.accept()

    def clickedRejectButton(self):
        self.reject()
