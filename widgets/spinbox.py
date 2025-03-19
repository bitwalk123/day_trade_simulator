from PySide6.QtCore import Qt, QMargins
from PySide6.QtWidgets import QSpinBox, QSizePolicy, QDoubleSpinBox


class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setStyleSheet("""
            QSpinBox {
                font-family: monospace;
                background-color: white;
                color: black;
                padding-left: 2px;
                padding-right: 2px;
            }
        """)
        self.setMinimumWidth(75)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        decimals = 5
        step_single = 0.00001

        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setStyleSheet("""
            QDoubleSpinBox {
                font-family: monospace;
                background-color: white;
                color: black;
                padding-left: 2px;
                padding-right: 2px;
            }
        """)
        self.setDecimals(decimals)
        self.setSingleStep(step_single)
        self.setMinimumWidth(75)
