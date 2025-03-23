from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QGridLayout


class GridLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )


class VBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
