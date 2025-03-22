from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid gray;
                border-radius: 3px;
                padding: 0px 18px 0px 3px;
            }
            QComboBox:editable {
                color: black;
                background: white;
            }
        """)