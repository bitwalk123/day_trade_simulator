from PySide6.QtWidgets import QFrame


class Frame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setLineWidth(1)