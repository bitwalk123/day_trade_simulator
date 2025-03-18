from PySide6.QtWidgets import QTabWidget


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

    def deleteAllTabs(self):
        n = self.count()
        for i in range(n):
            obj = self.widget(i)
            obj.deleteLater()

        # これだけで、問題ないとは思うが念のため、上で明示的に削除しておく
        self.clear()
