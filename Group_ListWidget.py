from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import add_group_Dialog
import re
import CS
import time
import threading

class Group_ListWidget(QListWidget):
    choose_group = pyqtSignal(str)
    group_info = []
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        self.doubleClicked.connect(self.choose_one_chat)

    def initDATA(self, top_group_info, id):
        self.group_info = top_group_info
        group_num = len(top_group_info)
        for i in range(group_num):
            item = QListWidgetItem()
            name = top_group_info[i]['group_name']
            iconpath = './res/' +  'group.jpg'
            font = QFont()
            font.setPointSize(16)

            item.setText(name)
            item.setIcon(QIcon(iconpath))
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)

            self.addItem(item)


    def choose_one_chat(self):
        for i in range(self.count()):
            item = self.item(i)
            item.setBackground(QColor('white'))

        items = self.selectedItems()
        for item in items:
            id = item.text()
            item.setBackground(QColor('blue'))
            self.choose_group.emit(id)

    def have_this_group(self, group):
        flag = False
        for i in range(self.count()):
            item = self.item(i)
            id = item.text()
            if group == id:
                flag = True
        return flag

    def add_unknown_group(self, id, member):
        font = QFont()
        font.setPointSize(16)
        iconpath = './res/group.jpg'
        item = QListWidgetItem()
        item.setText(id)
        item.setIcon(QIcon(iconpath))
        item.setFont(font)
        item.setTextAlignment(Qt.AlignCenter)
        self.addItem(item)
        data = {}
        data['group_name'] = id
        data['member'] = member
        self.group_info.append(data)


    def initUI(self):
        self.setIconSize(QSize(100,100))


    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            cmenu = QMenu(self)

            addAct = QAction('创建群聊', cmenu)
            cmenu.addAction(addAct)
            addAct.triggered.connect(self.add_group)

            deleteAct = QAction('删除群聊', cmenu)
            cmenu.addAction(deleteAct)
            deleteAct.triggered.connect(self.delete_group)
            cmenu.popup(self.mapToGlobal(event.pos()))

    def add_group(self, id=None):
        dg = add_group_Dialog.add_group_Dialog()
        answer = dg.exec()
        if answer > 0:
            item = QListWidgetItem()
            group_name = dg.group_name
            IDs = dg.member
            data = {}
            data['group_name'] = group_name
            data['member'] = IDs
            if id!=None:
                data['member'].append(id)
            self.group_info.append(data)
            iconpath = dg.get_iconpath()
            font = QFont()
            font.setPointSize(16)
            item.setText(group_name)
            item.setIcon(QIcon(iconpath))
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)
            self.addItem(item)


    def delete_group(self):
        del_items = self.selectedItems()
        for item in del_items:
            i = 0
            while i < len(self.group_info):
                if item.text() == self.group_info[i]['group_name']:
                    del self.group_info[i]
                else:
                    i += 1
            self.takeItem(self.row(item))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Group_ListWidget()
    sys.exit(app.exec_())



