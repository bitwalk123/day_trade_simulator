import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QSizePolicy

from structs.res import AppRes
from widgets.labels import LabelInt
from widgets.slider import Slider


class SelectButton(QPushButton):
    def __init__(self, name_color: str = 'blue'):
        super().__init__()
        self.label: LabelInt | None = None
        self.slider: Slider | None = None
        self.param = ''

        self.setFixedWidth(20)
        self.setFlat(True)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setStyleSheet("""
        QPushButton {
            background-color: %s;
        }
        """ % name_color)

    def setObjects(self, label: LabelInt, slider: Slider):
        self.label = label
        self.slider = slider

    def setObjectsDisabled(self, state: bool):
        self.label.setDisabled(state)
        self.slider.setDisabled(state)

    def setParam(self, param: str):
        self.param = param

    def getParam(self) -> str:
        return self.param

    def getLabel(self):
        return self.label

    def getLabelValue(self):
        return int(self.label.getValue())

class Button(QPushButton):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
        QPushButton {
            background-color: #fcfcfc;
        }
        """)

class EditButton(Button):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setIcon(
            QIcon(os.path.join(res.dir_image, 'pencil.png'))
        )
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )


class FolderButton(Button):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setIcon(
            QIcon(os.path.join(res.dir_image, 'folder.png'))
        )


class StartButton(Button):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setIcon(
            QIcon(os.path.join(res.dir_image, 'start.png'))
        )
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )
