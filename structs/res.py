import re


class AppRes:
    dir_config = 'conf'
    dir_excel = 'excel'
    dir_font = 'fonts'
    dir_image = 'images'
    dir_ohlc = 'ohlc'
    dir_result = 'results'
    dir_tick = 'tick'
    dir_transaction = 'transaction'

    # Excel ファイル名のパターン（デフォルト）
    default_excel_file_pattern = re.compile(r'^trader_[0-9]{8}\.xlsm$')
