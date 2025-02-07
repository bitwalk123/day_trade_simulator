from PySide6.QtWidgets import QPushButton


class SelectButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(20)
        self.setFlat(True)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setStyleSheet("""
        QPushButton {
            background-color: blue;
        }
        """)
