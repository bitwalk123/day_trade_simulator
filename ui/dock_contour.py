import pandas as pd
from PySide6.QtCore import QMargins, Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QDockWidget,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget, QSlider,
)

from structs.res import AppRes
from widgets.buttons import SelectButton
from widgets.labels import LabelTitle, LabelTitle2, LabelInt
from widgets.pads import HPadFixed


class DockContour(QDockWidget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        self.setMinimumWidth(400)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )
        self.layout_params = QGridLayout()

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        base = QWidget()
        self.setWidget(base)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        base.setLayout(layout)

        area = self.set_param_matrix()
        layout.addWidget(area)

        but_draw = QPushButton('プロット')
        layout.addWidget(but_draw)

    def set_param_matrix(self):
        area = QScrollArea()
        area.setWidgetResizable(True)

        base = QWidget()
        area.setWidget(base)

        layout = self.layout_params
        layout.setSpacing(0)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        base.setLayout(layout)

        return area

    def setParams(self, df: pd.DataFrame):
        r = 0
        head_name = LabelTitle2('Parameter')
        self.layout_params.addWidget(head_name, r, 0)

        head_value = LabelTitle2('V')
        head_value.setFixedWidth(30)
        self.layout_params.addWidget(head_value, r, 1)

        head_x = LabelTitle2('X')
        head_x.setFixedWidth(20)
        self.layout_params.addWidget(head_x, r, 3)

        head_y = LabelTitle2('Y')
        head_y.setFixedWidth(20)
        self.layout_params.addWidget(head_y, r, 4)

        pad = HPadFixed()
        self.layout_params.addWidget(pad, r, 5)

        r += 1
        self.group_x = group_x = QButtonGroup()
        self.group_y = group_y = QButtonGroup()

        for col in df.columns:
            if col == 'code':
                continue
            if col == 'date':
                continue
            if col == 'total':
                continue

            lab_name = LabelTitle(col)
            self.layout_params.addWidget(lab_name, r, 0)

            lab_value = LabelInt()
            self.layout_params.addWidget(lab_value, r, 1)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setFixedWidth(100)
            #slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
            #slider.setRange(0, 100)
            #slider.valueChanged.connect(self.show_value)
            self.layout_params.addWidget(slider, r, 2)

            but_x = SelectButton('#44f')
            group_x.addButton(but_x)
            self.layout_params.addWidget(but_x, r, 3)

            but_y = SelectButton('#f44')
            group_y.addButton(but_y)
            self.layout_params.addWidget(but_y, r, 4)

            pad = HPadFixed()
            self.layout_params.addWidget(pad, r, 5)
            r += 1
