from structs.app_enum import LoopStatus


class CounterLoop:
    def __init__(self):
        self.cnt_file = 0
        self.cnt_code = 0
        self.cnt_row = 0

        self.max_file = 0
        self.max_code = 0
        self.max_row = 0

    def getCountCode(self) -> int:
        return self.cnt_code

    def getCountCondition(self) -> int:
        return self.cnt_row + 1

    def getCountFile(self) -> int:
        return self.cnt_file

    def getCountRow(self) -> int:
        return self.cnt_row

    def getMaxCode(self) -> int:
        return self.max_code

    def getMaxFile(self) -> int:
        return self.max_file

    def getMaxRow(self) -> int:
        return self.max_row

    def increment(self):
        self.cnt_row += 1
        if self.max_row <= self.cnt_row:
            self.cnt_row = 0
            self.cnt_code += 1
            if self.max_code <= self.cnt_code:
                self.cnt_code = 0
                self.cnt_file += 1
                if self.max_file <= self.cnt_file:
                    return LoopStatus.COMPLETE
                else:
                    return LoopStatus.NEXT_FILE
            else:
                return LoopStatus.NEXT_CODE
        else:
            return LoopStatus.NEXT_CONDITION

    def setMaxAll(self, max_file: int, max_code: int, max_row: int):
        self.max_file = max_file
        self.max_code = max_code
        self.max_row = max_row

    def setMaxFile(self, max_file: int):
        self.max_file = max_file

    def setMaxCode(self, max_code: int):
        self.max_code = max_code

    def setMaxRow(self, max_row: int):
        self.max_row = max_row
