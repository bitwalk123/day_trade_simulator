from typing import Any, Union

import numpy as np
import pandas as pd
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt, QPersistentModelIndex,
)


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, df: pd.DataFrame, formats:list,parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.df = df
        self.formats = formats

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        """
        if parent == QModelIndex():
            return len(self._dataframe)
        return 0
        """
        return len(self.df)

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0
        """
        return len(self.df.columns)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        value = self.df.iloc[row, col]

        if role == Qt.ItemDataRole.DisplayRole:
            if self.formats[col] == 'int' and type(value) is not str:
                return '{:,}'.format(int(value))
            elif self.formats[col] == 'ts' and type(value) is not str:
                str_hh = '{:0=2}'.format(value.hour)
                str_mm = '{:0=2}'.format(value.minute)
                str_ss = '{:0=2}'.format(value.second)
                return '%s:%s:%s' % (str_hh, str_mm, str_ss)
            else:
                return str(value)

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if self.formats[col] == 'str' or self.formats[col] == 'ts':
                flag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            else:
                flag = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

            return flag

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.df.columns[section])

            if orientation == Qt.Orientation.Vertical:
                # return str(self._dataframe.index[section])
                return section + 1

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if orientation == Qt.Orientation.Vertical:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

        return None
