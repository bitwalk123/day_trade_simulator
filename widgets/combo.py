from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(100)
        self.setStyleSheet("""
            QComboBox:editable {
                font-family: monospace;
                color: black;
                background: white;
            }
        """)