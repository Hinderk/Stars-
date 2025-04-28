
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import QModelIndex

from defines import PlayerType as PT
from defines import AIMode as AI




class PlayerData(QAbstractTableModel):

    def __init__(self, people, pcount):
        super().__init__()
        self.uf_count = 0
        self.ex_count = 0
        self.ai_count = 0
        self.cp_count = {}
        self.number_of_players = pcount
        self.players = {}
        self.add_player(0, PT.HUP, None, people.my_faction())
        n = 1
        while n < self.number_of_players:
            self.add_player(n, PT.AIP, AI.AI1, people.random_faction())
            n += 1


    def add_player(self, row, ptype, pmode, pfaction):
        next_row = row + 1
        if self.number_of_players < next_row:
            self.beginInsertRows(QModelIndex(), next_row, next_row)
            self.number_of_players = next_row
            self.endInsertRows()
        if row in self.players:
            _, _, _, pname = self.players[row]
        elif ptype == PT.EXP:
            self.ex_count += 1
            pname = 'AI Stewarts ' + str(self.ex_count).zfill(2)
        elif ptype == PT.RNG:
            if pmode:
                self.ai_count += 1
                pname = 'AI Antagonists ' + str(self.ai_count).zfill(2)
            else:
                self.uf_count += 1
                pname = 'Unknown Actors ' + str(self.uf_count).zfill(2)
        else:
            pname = pfaction.name
            if pname in self.cp_count:
                self.cp_count[pname] += 1
            else:
                self.cp_count[pname] = 1
            pname += ' ' + str(self.cp_count[pname]).zfill(2)
        self.players[row] = (ptype, pmode, pfaction, pname)


    def remove_player(self, row):
        if row in self.players:
            self.beginRemoveRows(QModelIndex(), row, row)
            self.players.pop(row)
            self.number_of_players -= 1
            self.endRemoveRows()
        n = 0
        target = {}
        for key in self.players:
            target[n] = self.players[key]
            n += 1
        self.players = target


    def reset_model(self, people, pcount):
        self.uf_count = 0
        self.ex_count = 0
        self.ai_count = 0
        self.cp_count.clear()
        self.beginResetModel()
        self.number_of_players = pcount
        self.players.clear()
        self.add_player(0, PT.HUP, None, people.my_faction())
        n = 1
        while n < pcount:
            self.add_player(n, PT.AIP, AI.AI1, people.random_faction())
            n += 1
        self.endResetModel()


    def rowCount(self, index):
        return self.number_of_players + 1


    def columnCount(self, index):
        return 3


    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            if row in self.players:
                t, m, f, _ = self.players[row]
                self.players[row] = (t, m, f, value)
                return True
        return False


    def data(self, index, role):
        """ Return either the content or the alignment for the indexed cell """
        col = index.column()
        row = index.row()
        if role == Qt.ItemDataRole.TextAlignmentRole:
            align = Qt.AlignmentFlag.AlignLeft
            if col < 2:
                align = Qt.AlignmentFlag.AlignHCenter
            return align | Qt.AlignmentFlag.AlignVCenter
        content = None
        if role == Qt.ItemDataRole.DisplayRole:
            content = ''
            if row in self.players:
                t, m, f, content = self.players[row]
                if col == 0:
                    if m:
                        content = 'AI (' + m.value + ')'
                    elif t == PT.RNG:
                        content = 'Human Player'
                    else:
                        content = t.value
                elif col == 1:
                    if t == PT.RNG:
                        content = 'Random Choice'
                    else:
                        content = f.species
        return content


    def flags(self, index):
        if index.isValid():
            flags = super().flags(index)
            if index.column() == 2 and index.row() in self.players:
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
