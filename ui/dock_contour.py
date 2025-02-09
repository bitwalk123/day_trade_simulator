import numpy as np
import pandas as pd
from PySide6.QtCore import QMargins, Qt, QObject
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
from widgets.labels import (
    LabelInt,
    LabelTitle,
    LabelTitle2,
)
from widgets.pads import HPadFixed
from widgets.slider import Slider


class DockContour(QDockWidget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res
        self.group_y = None
        self.group_x = None

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
        group_x.buttonToggled.connect(self.selected_button)
        group_y.buttonToggled.connect(self.selected_button)

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

            slider = Slider(Qt.Orientation.Horizontal)
            slider.setLabel(lab_value)
            slider.setFixedWidth(100)
            slider.setTickPosition(
                QSlider.TickPosition.TicksBothSides
            )
            slider.setRange(
                int(df[col].min()),
                int(df[col].max())
            )
            slider.setValue(int(df[col].median()))
            slider.valueChanged.connect(self.show_value)
            self.layout_params.addWidget(slider, r, 2)

            but_x = SelectButton('#44f')
            but_x.setParam(col)
            but_x.setObjects(lab_value, slider)
            group_x.addButton(but_x, r)
            self.layout_params.addWidget(but_x, r, 3)

            but_y = SelectButton('#f44')
            but_y.setParam(col)
            but_y.setObjects(lab_value, slider)
            group_y.addButton(but_y, r)
            self.layout_params.addWidget(but_y, r, 4)

            pad = HPadFixed()
            self.layout_params.addWidget(pad, r, 5)
            r += 1

        group_x.button(1).setChecked(True)
        group_y.button(2).setChecked(True)

    def show_value(self, value):
        slider: Slider | QObject = self.sender()
        slider.setLabelValue(value)

    def selected_button(self, obj: SelectButton, flag):
        # print(obj.getParam(), flag)
        obj.setObjectsDisabled(flag)
