from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QSizePolicy

from structs.res import AppRes
from widgets.checks import Switch
from widgets.container import Widget, PadH, PadHFixed
from widgets.labels import LabelTitle
from widgets.layouts import HBoxLayout
from widgets.spinbox import SpinBox


class PanelLossCut(Widget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setContentsMargins(QMargins(0, 0, 0, 0))

        layout = HBoxLayout()
        self.setLayout(layout)

        sep1 = PadHFixed(10)
        layout.addWidget(sep1)

        self.sw_losscut = sw_losscut = Switch()
        sw_losscut.set(False)
        sw_losscut.statusChanged.connect(self.on_status_changed)
        layout.addWidget(sw_losscut)

        sep2 = PadHFixed(20)
        layout.addWidget(sep2)

        self.lab_losscut_factor = lab_losscut_factor = LabelTitle('損切因数')
        lab_losscut_factor.setDisabled(True)
        layout.addWidget(lab_losscut_factor)

        self.sb_losscut_factor = sb_losscut_factor = SpinBox()
        sb_losscut_factor.setValue(3)
        sb_losscut_factor.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sb_losscut_factor.setFixedWidth(60)
        sb_losscut_factor.setDisabled(True)
        layout.addWidget(sb_losscut_factor)

        hpad = PadH()
        layout.addWidget(hpad)

    def getLossCutFactor(self) -> int:
        return self.sb_losscut_factor.value()

    def IsLossCutEnabled(self) -> bool:
        return self.sw_losscut.isON()

    def on_status_changed(self, status):
        self.lab_losscut_factor.setEnabled(status)
        self.sb_losscut_factor.setEnabled(status)
