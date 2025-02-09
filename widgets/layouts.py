from PySide6.QtWidgets import QVBoxLayout


class VBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
