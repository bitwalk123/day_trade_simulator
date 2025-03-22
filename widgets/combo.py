from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox:editable {
                color: black;
                background: white;
            }
        """)