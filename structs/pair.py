class PairXY():
    def __init__(self, ts, x, y):
        self.ts = ts
        self.list_x = list()
        self.list_y = list()
        self.appendXY(x, y)

    def appendXY(self, x, y):
        self.list_x.append(x)
        self.list_y.append(y)

    def length(self):
        return len(self.list_x)

    def getTimeStamp(self):
        return self.ts

    def getX(self):
        return self.list_x

    def getY(self):
        return self.list_y
