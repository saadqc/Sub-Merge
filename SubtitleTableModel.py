from PyQt4 import QtGui, QtCore
import sys


class SubtitleTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[], headers=[], parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__data = data
        self.__headers = headers

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        return 3

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):

        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            row = index.row()
            column = index.column()
            value = self.__data[row]

            if column == 0:
                return value.index
            elif column == 1:
                return '{} --> {}'.format(str(value.start), str(value.end))
            else:
                return value.text

    def get_data(self):
        return self.__data

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:

            row = index.row()
            column = index.column()

            color = QtGui.QColor(value)

            if color.isValid():
                self.__data[row][column] = color
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:

                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return ""
            else:
                return QtCore.QString("Color %1").arg(section)

    # =====================================================#
    # INSERTING & REMOVING
    # =====================================================#
    def insertRows(self, position, rows, item, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.__data.insert(position, item)

        self.endInsertRows()

        return True

    def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
        self.__data = self.__data[:position] + self.__data[position + rows:]
        self.endRemoveRows()

        return True
