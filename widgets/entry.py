from PySide6.QtWidgets import QLineEdit, QSizePolicy


class Entry(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFrame(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(75)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred
        )
        self.setStyleSheet("""
            QLineEdit {
                font-family: monospace;
                background-color: white;
                color: black;
                padding-left:5px;
            }
        """)

class EntryExcelFile(Entry):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(100)
