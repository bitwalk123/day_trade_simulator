import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import QPushButton, QSizePolicy, QToolButton, QStyleOptionButton, QStyle

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


class EditButton(Button):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setIcon(
            QIcon(os.path.join(res.dir_image, 'pencil.png'))
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setToolTip('編集')


class FolderButton(Button):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setIcon(
            QIcon(os.path.join(res.dir_image, 'folder.png'))
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred
        )


class FolderToolButton(QToolButton):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setIcon(
            QIcon(os.path.join(res.dir_image, 'folder.png'))
        )


class PushButton(QPushButton):
    """
    アイコンサイズをボタンの大きさに応じて動的に変更するプッシュボタン
    Reference:
    https://stackoverflow.com/questions/31742194/dynamically-resize-qicon-without-calling-setsizeicon
    """

    def __init__(self, label=None, parent=None):
        super(PushButton, self).__init__(label, parent)

        self.pad = 4  # padding between the icon and the button frame
        self.minSize = 8  # minimum size of the icon

        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setSizePolicy(sizePolicy)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        # ---- get default style ----

        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        # ---- scale icon to button size ----

        # Rect = opt.rect
        Rect = opt.rect

        h = Rect.height()
        w = Rect.width()
        iconSize = max(min(h, w) - 2 * self.pad, self.minSize)

        opt.iconSize = QSize(iconSize, iconSize)

        # ---- draw button ----

        self.style().drawControl(QStyle.ControlElement.CE_PushButton, opt, qp, self)

        qp.end()


class StartButton(PushButton):
    def __init__(self, res: AppRes):
        super().__init__()
        icon = QIcon(os.path.join(res.dir_image, 'start.png'))
        self.setIcon(icon)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred
        )
        self.setToolTip('スタート')
