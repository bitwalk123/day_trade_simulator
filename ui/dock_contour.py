import pandas as pd
from PySide6.QtCore import QMargins, Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QGridLayout,
    QScrollArea,
    QWidget, QSizePolicy, QButtonGroup,
)

from structs.res import AppRes
from widgets.buttons import SelectButton
from widgets.labels import LabelTitle, LabelTitle2
from widgets.pads import HPadFixed


class DockContour(QDockWidget):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # UI
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        self.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        #sa.setHorizontalScrollBarPolicy(
        #    Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        #)
        self.setWidget(sa)

        self.base_params = base_params = QWidget()
        self.setMinimumWidth(300)

        """
        base_params.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )
        """
        sa.setWidget(base_params)

        self.layout_params = layout_params = QGridLayout()
        layout_params.setSpacing(0)
        layout_params.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        layout_params.setContentsMargins(QMargins(0, 0, 0, 0))
        base_params.setLayout(layout_params)

    def set_params(self, df: pd.DataFrame):
        r = 0
        head_name = LabelTitle2('Parameter')
        self.layout_params.addWidget(head_name, r, 0)
        head_x = LabelTitle2('X')
        head_x.setFixedWidth(20)
        self.layout_params.addWidget(head_x, r, 1)
        head_y = LabelTitle2('Y')
        head_y.setFixedWidth(20)
        self.layout_params.addWidget(head_y, r, 2)
        pad = HPadFixed()
        self.layout_params.addWidget(pad, r, 3)
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
            but_x = SelectButton()
            group_x.addButton(but_x)
            self.layout_params.addWidget(but_x, r, 1)
            but_y = SelectButton()
            group_y.addButton(but_y)
            self.layout_params.addWidget(but_y, r, 2)
            pad = HPadFixed()
            self.layout_params.addWidget(pad, r, 3)
            r += 1

