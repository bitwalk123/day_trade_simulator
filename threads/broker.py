import os

from PySide6.QtCore import (
    QObject,
    QThreadPool,
    Signal,
)
from PySide6.QtWidgets import QProgressBar

from structs.app_enum import LoopStatus
from structs.res import AppRes
from threads.counter import CounterLoop
from threads.preprocs import WorkerPrepDataset
from ui.dock_executor import DockExecutor
from ui.win_executor import WinExecutor
from ui.win_main import WinMain


class BrokerThreadLoop(QObject):
    errorMessage = Signal(str)
    threadFinished = Signal(bool)

    def __init__(
            self,
            res: AppRes,
            threadpool: QThreadPool,
            dock: DockExecutor,
            win: WinExecutor,
            pbar: QProgressBar
    ):
        super().__init__()
        self.res = res
        self.threadpool = threadpool
        self.dock = dock
        self.panel = win
        self.pbar = pbar

        self.winmain = None
        self.output_dir = None
        self.list_target = None

        # シミュレーション対象の Excel ファイルを取得
        self.dir, self.files = dock.getExcelFiles()

        # ループカウンタ
        self.counter = CounterLoop()
        self.counter.setMaxFile(len(self.files))

        self.dict_dict_target = dict()

    def create_winmain(self, dict_target):
        if self.winmain is not None:
            self.winmain.deleteLater()
        self.winmain = WinMain(self.res, dict_target, self.threadpool, self.pbar)
        self.winmain.simulationCompleted.connect(self.loop_simulation_next)
        self.winmain.setFixedSize(1600, 800)
        self.winmain.show()

    def getDir(self) -> str:
        return self.dir

    def getFiles(self) -> list:
        return self.files

    def loop_simulation(self):
        """
        シミュレーションのメイン処理
        シミュレータに条件を書き込んでシミュレーターを起動する処理
        """
        n_condition = self.counter.getCountCondition()
        af_init = self.panel.getAFinit(n_condition)
        af_step = self.panel.getAFstep(n_condition)
        af_max = self.panel.getAFmax(n_condition)

        self.winmain.dock.objAFinit.setValue(af_init)
        self.winmain.dock.objAFstep.setValue(af_step)
        self.winmain.dock.objAFmax.setValue(af_max)

        if self.panel.panelLossCut.IsLossCutEnabled():
            self.winmain.dock.setLossCutEnabled(True)
        else:
            self.winmain.dock.setLossCutEnabled(False)

        self.winmain.autoSimulationStart()

    def loop_simulation_init(self):
        """
        シミュレーション・ループの最初
        1. スレッドで Excel ファイルを読み込み、
        2. シミュレーションに必要なデータセットを準備する処理
        """
        file_excel = str(os.path.join(self.dir, self.files[self.counter.getCountFile()]))
        self.panel.setSrcFile(file_excel)

        prep_ds = WorkerPrepDataset(file_excel)
        prep_ds.updateProgress.connect(self.on_status_update)
        prep_ds.threadFinished.connect(self.on_excel_read_completed)
        self.threadpool.start(prep_ds)

    def loop_simulation_next(self, dict_result: dict):
        """
        ある条件のシミュレーション終わって、次の処理を決める分岐点
        """
        # プロットの保存
        dir_save = str(os.path.join(self.output_dir, dict_result['date']))
        if not os.path.isdir(dir_save):
            os.mkdir(dir_save)

        name_chart = 'chart_{:s}_{:0>3d}.png'.format(
            self.list_target[self.counter.getCountCode()]['code'],
            self.counter.getCountCondition()
        )
        name_chart = os.path.join(dir_save, name_chart)
        self.winmain.saveChart(name_chart)

        # 結果を標準出力
        print(
            self.list_target[self.counter.getCountCode()]['code'],
            self.counter.getCountCondition(),
            dict_result['total']
        )

        # 結果の処理
        self.panel.setTotal(self.counter.getCountCondition(), dict_result['total'])

        # カウンタ・インスタンスのインクリメント
        result: LoopStatus = self.counter.increment()
        # インクリメントした結果に応じて処理を分岐
        if result == LoopStatus.NEXT_CONDITION:
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # NEXT_CONDITION
            # 次の水準の条件へ（単純ループ）
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # シミュレーション・ループへ
            self.loop_simulation()
        else:
            # -----------------------------------------------
            # １銘柄について全ての水準のシュミレーション終了時の共通処理
            # -----------------------------------------------
            # 全条件の Total を保存（とりあえず HTML のテーブル形式）
            name_html = 'summary_{:s}_{:s}.html'.format(
                dict_result['date'],
                self.list_target[self.counter.getCountCode()]['code']
            )
            name_html = os.path.join(dir_save, name_html)
            self.panel.saveResult(name_html)

            # 水準表の Total（収益）をクリア
            self.panel.clearTotal()

            # Excel 内の銘柄 (CODE) のシミュレーション全てが終わったか？
            if result == LoopStatus.NEXT_CODE:
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # NEXT_CODE
                # Excel 内の次の銘柄 (CODE) のシミュレーションへ進む
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                dict_target = self.list_target[self.counter.getCountCode()]
                # シミュレーションを新たな銘柄 (CODE) 用に再起動
                self.create_winmain(dict_target)
                # シミュレーション・ループへ
                self.loop_simulation()
            elif result == LoopStatus.NEXT_FILE:
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # NEXT_FILE
                # 新たな Excel ファイルの読み込みから
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                self.loop_simulation_init()
            elif result == LoopStatus.COMPLETE:
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # COMPLETE
                # 全てのファイル、銘柄、水準についてシミュレーション終了
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                if self.winmain is not None:
                    self.winmain.deleteLater()
                print('complete simulation')
            else:
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # Unknown
                # 不明なステータスで終了（念のため）
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                print('complete simulation with unknown status')

    def start(self):
        # Excel ファイルの確認
        if self.counter.getMaxFile() == 0:
            msg = '### Excel ファイルが選択されていません。'
            self.errorMessage.emit(msg)
            self.threadFinished.emit(False)
            return

        # 出力先ディレクトリの確認
        output_dir = self.panel.getOutputDir()
        if output_dir == '':
            msg = '### 出力先ディレクトリが設定されていません。'
            self.errorMessage.emit(msg)
            self.threadFinished.emit(False)
            return
        else:
            self.output_dir = output_dir

        # 水準数を設定
        self.counter.setMaxRow(self.panel.getLevelMax())

        # ループの初期設定
        self.loop_simulation_init()

    def on_excel_read_completed(self, list_target):
        """
        Excel ファイルを読み込んだ後、
        データセットに基づき、銘柄毎のタブ画面を作成
        :param list_target:
        :return:
        """
        print(self.files[self.counter.getCountFile()])

        # ターゲット銘柄のリストを保持
        self.list_target = list_target

        # 銘柄数の設定
        self.counter.setMaxCode(len(list_target))

        # シミュレータウィンドウの表示
        dict_target = list_target[0]
        self.create_winmain(dict_target)

        # シミュレーション・ループ
        self.loop_simulation()

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)
