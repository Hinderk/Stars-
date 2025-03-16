
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import QModelIndex

from defines import PlayerType as PT
from defines import AIMode as AI




class PlayerData(QAbstractTableModel):


    def __init__(self):
        super(self.__class__, self).__init__()
        self.NumberOfPlayers = 0
        self.Players = dict()


    def AddPlayer(self, row, ptype, pmode, pfaction):
        NextRow = row + 1
        if self.NumberOfPlayers < NextRow:
            self.beginInsertRows(QModelIndex(), NextRow, NextRow)
            self.NumberOfPlayers = NextRow
            self.endInsertRows()
        if row in self.Players:
            _, _, _, pname = self.Players[row]
        elif ptype == PT.EXP:
            pname = 'AI Stewart for Human Absentee'
        elif ptype == PT.RNG:
            if pmode:
                pname = 'Undisclosed AI Antagonist'
            else:
                pname = 'Unknown Faction'
        else:
            pname = pfaction.Name
        self.Players[row] = (ptype, pmode, pfaction, pname)


    def RemovePlayer(self, row):
        if row in self.Players:
            self.beginRemoveRows(QModelIndex(), row, row)
            self.Players.pop(row)
            self.NumberOfPlayers -= 1
            self.endRemoveRows()
        n = 0
        Target = dict()
        for key in self.Players:
            Target[n] = self.Players[key]
            n += 1
        self.Players = Target


    def rowCount(self, index):
        return self.NumberOfPlayers + 1

    def columnCount(self, index):
        return 3


    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            if row in self.Players:
                t, m, f, _ = self.Players[row]
                self.Players[row] = (t, m, f, value)
                return True
        return False


    def data(self, index, role):
        col = index.column()
        row = index.row()
        if role == Qt.ItemDataRole.TextAlignmentRole:
            align = Qt.AlignmentFlag.AlignLeft
            if col < 2:
                align = Qt.AlignmentFlag.AlignHCenter
            return align | Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.DisplayRole:
            if row in self.Players:
                t, m, f, name = self.Players[row]
                if col == 0:
                    if m:
                        return 'AI (' + m.value + ')'
                    if t == PT.RNG:
                        return 'Human Player'
                    return t.value
                if col == 1:
                    if t == PT.RNG:
                        return 'Random Choice'
                    return f.Species
                return name
            return ''
        return None


    def flags(self, index):
        if index.isValid():
            flags = super().flags(index)
            if index.column() == 2 and index.row() in self.Players:
                flags |= Qt.ItemFlag.ItemIsEditable
            flags &= ~Qt.ItemFlag.ItemIsSelectable
            return flags
        return Qt.ItemFlag.ItemIsEnabled


    def headerData(self, index, hv, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if hv == Qt.Orientation.Horizontal:
                if index == 0:
                    return 'Slot'
                if index == 1:
                    return 'Faction'
                return 'Player Name'
            return str(index + 1)
        return None
