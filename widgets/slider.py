from PySide6.QtWidgets import QSlider

from widgets.labels import LabelInt


class Slider(QSlider):
    def __init__(self, *args):
        super().__init__(*args)
        self.setTickInterval(1)
        self.label: LabelInt | None = None

    def setLabel(self, label: LabelInt):
        self.label = label

    def setValue(self, value: int):
        super().setValue(value)
        self.setLabelValue(value)

    def setLabelValue(self, value: int):
        self.label.setValue(value)
