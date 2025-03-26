from PySide6.QtCore import Qt, QMargins
from PySide6.QtWidgets import QCheckBox


class CheckBox(QCheckBox):
    def __init__(self):
        super().__init__()

class CheckBoxLossCut(CheckBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QCheckBox {
                margin-top: 4px;
                margin-left: 10px;
            }
        """)