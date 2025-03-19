from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)

from funcs.preprocs import (
    read_sheet_cover,
    read_sheet_cover_params,
    read_sheet_tick,
)


class PrepDatasetSignal(QObject):
    threadFinished = Signal(list)
    updateProgress = Signal(int)


class WorkerPrepDataset(QRunnable, PrepDatasetSignal):
    def __init__(self, file_excel: str):
        super().__init__()
        self.file_excel = file_excel

    def run(self):
        list_target = list()

        file_excel = self.file_excel
        df_cover = read_sheet_cover(self.file_excel)
        # ワークシート Cover の列数
        n = len(df_cover.columns)
        # -------------
        # 🔆 進捗更新通知
        # -------------
        self.updateProgress.emit(int(100. * 1 / (n + 1)))

        # 銘柄毎にループ
        for col in range(n):
            dict_target = dict()

            # シート Cover から個別銘柄の情報を取得
            code, date = read_sheet_cover_params(df_cover, col, dict_target)

            # -------------
            # 🔆 進捗更新通知
            # -------------
            self.updateProgress.emit(int(100. * (1 + col + 0.5) / (n + 1)))

            # 銘柄コードから、ティックデータ用ワークシート名を特定しティックデータを読み込む
            read_sheet_tick(file_excel, code, date, dict_target)

            # -------------
            # 🔆 進捗更新通知
            # -------------
            self.updateProgress.emit(int(100. * (1 + col + 1) / (n + 1)))

            list_target.append(dict_target)

        # ------------------
        # 🔆 スレッド収量の通知
        # ------------------
        self.threadFinished.emit(list_target)
