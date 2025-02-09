from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QSizePolicy,
)


class LabelDate(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(
            QFrame.Shape.Panel | QFrame.Shadow.Sunken
        )
        self.setLineWidth(1)
        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                background-color: white;
            }
        """)


class LabelFlat(QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.setLineWidth(1)
        self.setStyleSheet('QLabel {font-family: monospace;}')

class LabelUnit(LabelFlat):
    def __init__(self, title: str):
        super().__init__(title)
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                padding-left: 5px;
            }
        """)

class LabelRight(QLabel):
    def __init__(self):
        super().__init__()
        self.setLineWidth(1)
        self.setStyleSheet('QLabel {font-family: monospace;}')
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )


class LabelString(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(
            QFrame.Shape.Panel | QFrame.Shadow.Sunken
        )
        self.setLineWidth(1)
        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                background-color: white;
            }
        """)


class LabelTitle(QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self.setFrameStyle(
            QFrame.Shape.Panel | QFrame.Shadow.Raised
        )
        self.setLineWidth(1)
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                padding-right: 5px;
            }
        """)

class LabelTitle2(LabelTitle):
    def __init__(self, title: str):
        super().__init__(title)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self.setFrameStyle(
            QFrame.Shape.Panel | QFrame.Shadow.Raised
        )
        self.setLineWidth(1)
        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                padding-right: 5px;
            }
        """)


class LabelTime(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(
            QFrame.Shape.Panel | QFrame.Shadow.Sunken
        )
        self.setLineWidth(1)
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                background-color: white;
            }
        """)


class LabelValue(QLabel):
    def __init__(self):
        super().__init__()
        self.flag = True
        self.setFrameStyle(
            QFrame.Shape.Panel | QFrame.Shadow.Sunken
        )
        self.setMinimumWidth(100)
        self.setLineWidth(1)
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                background-color: white;
                padding-right: 2px;
            }
        """)

    def getValue(self) -> int | float:
        if self.flag:
            return float(self.text())
        else:
            return int(self.text())

    def setValue(self, value: int | float, flag=True):
        self.flag = flag
        if flag:
            self.setText('%.1f' % float(value))
        else:
            self.setText('%d' % int(value))

class LabelValue2(LabelValue):
    def __init__(self):
        super().__init__()

    def setValue(self, value: int | float, flag=True):
        self.flag = flag
        if flag:
            self.setText('%.3f' % float(value))
        else:
            self.setText('%d' % int(value))

class LabelInt(QLabel):
    def __init__(self):
        super().__init__()
        self.flag = True
        self.setFrameStyle(
            QFrame.Shape.Panel | QFrame.Shadow.Sunken
        )
        self.setMinimumWidth(1)
        self.setLineWidth(1)
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                font-family: monospace;
                background-color: white;
                padding-right: 2px;
            }
        """)

    def getValue(self) -> int:
        return int(self.text())

    def setValue(self, value: int):
        self.setText('%d' % int(value))
