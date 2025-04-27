class CounterLoop:
    def __init__(self):
        self.cnt_file = 0
        self.cnt_code = 0
        self.cnt_row = 0

        self.max_file = 0
        self.max_code = 0
        self.max_row = 0

    def getMaxFile(self) -> int:
        return self.max_file

    def getMaxCode(self) -> int:
        return self.max_code

    def getMaxRow(self) -> int:
        return self.max_row

    def setMaxAll(self, max_file: int, max_code: int, max_row: int):
        self.max_file = max_file
        self.max_code = max_code
        self.max_row = max_row

    def setMaxFile(self, max_file: int):
        self.max_file = max_file

    def setMaxCode(self, max_code: int):
        self.max_code = max_code

    def setMaxRow(self, max_row: int):
        self.max_code = max_row
