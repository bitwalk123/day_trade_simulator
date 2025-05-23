from PySide6.QtCore import Qt, Signal, QRect, QPropertyAnimation, Property, QSize
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QPushButton,
    QSizePolicy, QAbstractButton,
)


class CheckBox(QCheckBox):
    def __init__(self):
        super().__init__()


class CheckBoxLossCut(CheckBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QCheckBox {
                margin-top: 4px;
                margin-left: 10px;
            }
        """)


class CheckBoxFile(QCheckBox):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.setStyleSheet("""
            QCheckBox {
                font-family: monospace;
            }
        """)


class Switch(QAbstractButton):
    """Implementation of a clean looking toggle switch translated from
    https://stackoverflow.com/a/38102598/1124661
    QAbstractButton::setDisabled to disable
    """
    statusChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        # self.onBrush = QBrush(QColor("#569167"))
        # self.slotBrush = QBrush(QColor("#999999"))
        # self.switchBrush = self.slotBrush
        # self.disabledBrush = QBrush(QColor("#666666"))
        self.onBrush = QBrush(QColor('#00b0b0'))
        self.slotBrush = QBrush(QColor('#999999'))
        self.switchBrush = self.slotBrush
        self.disabledBrush = QBrush(QColor('#404040'))

        self.on = False
        self.fullHeight = 18
        self.halfHeight = self.xPos = int(self.fullHeight / 2)
        self.fullWidth = 34
        self.setFixedWidth(self.fullWidth)
        self.slotMargin = 3
        self.slotHeight = self.fullHeight - 2 * self.slotMargin
        self.travel = self.fullWidth - self.fullHeight
        self.slotRect = QRect(
            self.slotMargin,
            self.slotMargin,
            self.fullWidth - 2 * self.slotMargin,
            self.slotHeight,
        )
        self.animation = QPropertyAnimation(self, b'pqProp', self)
        self.animation.setDuration(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def paintEvent(self, e):
        """QAbstractButton method. Paint the button.
        """
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.switchBrush if self.on else self.disabledBrush)
        painter.setOpacity(0.6)
        painter.drawRoundedRect(
            self.slotRect, self.slotHeight / 2, self.slotHeight / 2,
        )
        painter.setOpacity(1.0)
        painter.drawEllipse(
            QRect(self.xPos, 0, self.fullHeight, self.fullHeight, )
        )

    def mouseReleaseEvent(self, e):
        """Switch the button.
        """
        if e.button() == Qt.MouseButton.LeftButton:
            self.on = not self.on
            self.switchBrush = self.onBrush if self.on else self.slotBrush
            self.animation.setStartValue(self.xPos)
            self.animation.setEndValue(self.travel if self.on else 0)
            self.animation.start()
            self.statusChanged.emit(self.on)
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        """Required to be implemented and return the size of the widget.
        """
        return QSize(self.fullWidth, self.fullHeight)

    def setOffset(self, o):
        """Setter for QPropertyAnimation.
        """
        self.xPos = o
        self.update()

    def getOffset(self):
        """Getter for QPropertyAnimation.
        """
        return self.xPos

    pqProp = Property(int, fget=getOffset, fset=setOffset)

    def set(self, on):
        """Set state to on, and trigger repaint.
        """
        self.on = on
        self.switchBrush = self.onBrush if on else self.slotBrush
        self.xPos = self.travel if on else 0
        self.update()

    def isON(self) -> bool:
        return self.on
