from PySide6.QtWidgets import QDockWidget

from structs.res import AppRes


class DockExecutor(QDockWidget):

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
