from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)
import pandas as pd
import yfinance as yf


def read_sheet_cover(file_excel: str) -> pd.DataFrame:
    # ワークシート Cover の読み込み
    name_sheet_cover = 'Cover'
    df = pd.read_excel(
        file_excel,
        sheet_name=name_sheet_cover,
        header=None,
        index_col=0,
    )
    return df


def get_cover_params(df_cover: pd.DataFrame, col: int, dict_target: dict) -> tuple[str, str]:
    # 銘柄コード
    row = list(df_cover.index).index('銘柄コード')
    code = df_cover.iloc[row, col]
    dict_target['code'] = code
    # Yahoo Finance から会社名を取得
    symbol = '%s.T' % code
    ticker = yf.Ticker(symbol)
    name = ticker.info['longName']
    dict_target['name'] = name
    # 現在日付の保持
    row = list(df_cover.index).index('現在日付')
    date = df_cover.iloc[row, col].replace('/', '-')
    dict_target['date'] = date
    # 呼び値
    row = list(df_cover.index).index('呼値')
    price_tick_min = df_cover.iloc[row, col]
    dict_target['price_tick_min'] = price_tick_min
    # AF（初期値）
    row = list(df_cover.index).index('AF（初期値）')
    af_init = df_cover.iloc[row, col]
    dict_target['af_init'] = af_init
    # AF（ステップ）
    row = list(df_cover.index).index('AF（ステップ）')
    af_step = df_cover.iloc[row, col]
    dict_target['af_step'] = af_step
    # AF（最大値）
    row = list(df_cover.index).index('AF（最大値）')
    af_max = df_cover.iloc[row, col]
    dict_target['af_max'] = af_max
    return code, date


def get_tick_data(file_excel: str, code: str, date: str, dict_target: dict):
    name_sheet_tick = 'tick_%s' % code
    df = pd.read_excel(
        file_excel,
        sheet_name=name_sheet_tick,
        header=0,
    )
    # 時刻データを日付を含んだ Matplotlib で扱える形式に変換、インデックスへ
    df.index = [pd.to_datetime('%s %s' % (date, t)) for t in df['Time']]
    df.index.name = 'Datetime'
    df = df[['Price', 'TREND', 'EP', 'AF', 'PSAR']]
    dict_target['tick'] = df


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
        # 進捗更新
        self.updateProgress.emit(int(100. * 1 / (n + 1)))

        # 銘柄毎にループ
        for col in range(n):
            dict_target = dict()

            # シート Cover から個別銘柄の情報を取得
            code, date = get_cover_params(df_cover, col, dict_target)
            # 進捗更新
            self.updateProgress.emit(int(100. * (1 + col + 0.5) / (n + 1)))

            # 銘柄コードから、ティックデータ用ワークシート名を特定しティックデータを読み込む
            get_tick_data(file_excel, code, date, dict_target)
            # 進捗更新
            self.updateProgress.emit(int(100. * (1 + col + 1) / (n + 1)))

            list_target.append(dict_target)

        self.threadFinished.emit(list_target)
