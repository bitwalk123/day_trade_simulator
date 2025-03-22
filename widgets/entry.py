from PySide6.QtWidgets import QLineEdit


class Entry(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFrame(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(75)
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                padding-left:5px;
            }
        """)
