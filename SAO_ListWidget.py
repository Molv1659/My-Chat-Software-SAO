from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import add_friend_Dialog
import re
import CS
import time
import threading

class SAO_ListWidget(QListWidget):
    choose_friend = pyqtSignal(str)
    endstate = False

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        t = threading.Thread(target = self.my_timer)
        t.start()
        self.doubleClicked.connect(self.choose_one_chat)


    def choose_one_chat(self):
        for i in range(self.count()):
            item = self.item(i)
            item.setBackground(QColor('white'))

        items = self.selectedItems()
        for item in items:
            id = item.text()
            item.setBackground(QColor('blue'))
            state = ( id.find('不')>-1 )
            if not state:
                id = re.findall(r'\d{10}', item.text())[0]
                self.rcv_label(id)
                self.choose_friend.emit(id)
            else:
                QMessageBox.information(self, 'Sorry', '本程序暂不支持发送离线消息，请找在线的好友聊天')


    def my_timer(self):
        while not self.endstate:
            time.sleep(0.1)
            self.update_friend_state()

    def end(self):
        self.endstate = True


    def update_friend_state(self):
        for i in range(self.count()):
            item = self.item(i)
            front = ''
            if item.text()[0] == '*':
                front = '*'
            id = re.findall(r'\d{10}', item.text())[0]
            answer = CS.query_state(id)
            if answer == 'n':
                item.setText(front + id + '(不在线)')
            else:
                item.setText(front + id + '(在线)')

    def have_this_friend(self, friend):
        flag = False
        for i in range(self.count()):
            item = self.item(i)
            id = re.findall(r'\d{10}', item.text())[0]
            if friend == id:
                flag = True
        return flag

    def add_unknown_friend(self, id):
        font = QFont()
        font.setPointSize(16)
        iconpath = './res/default.jpg'
        item = QListWidgetItem()
        item.setText(id)
        item.setIcon(QIcon(iconpath))
        item.setFont(font)
        item.setTextAlignment(Qt.AlignCenter)
        self.addItem(item)

    def un_rcv_label(self, friend):
        for i in range(self.count()):
            item = self.item(i)
            id = re.findall(r'\d{10}', item.text())[0]
            if friend == id:
                id = '*' + item.text()
                item.setText(id)

    def rcv_label(self, friend):
        for i in range(self.count()):
            item = self.item(i)
            id = re.findall(r'\d{10}', item.text())[0]
            temp_text = item.text()
            while friend == id and temp_text[0]=='*':
                temp_text = temp_text[1:]
            item.setText(temp_text)




    def initDATA(self, friend_info, id):
        friend_num = len(friend_info)
        for i in range(friend_num):
            item = QListWidgetItem()
            name = friend_info[i]['id']
            iconpath = './res/' + str(i) + '.jpg'
            font = QFont()
            font.setPointSize(16)

            item.setText(name)
            item.setIcon(QIcon(iconpath))
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)

            self.addItem(item)


    def initUI(self):
        self.setIconSize(QSize(100,100))


    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            cmenu = QMenu(self)

            addAct = QAction('填加好友', cmenu)
            cmenu.addAction(addAct)
            addAct.triggered.connect(self.add_friend)

            deleteAct = QAction('删除好友', cmenu)
            cmenu.addAction(deleteAct)
            deleteAct.triggered.connect(self.delete_friend)
            cmenu.popup(self.mapToGlobal(event.pos()))

    def add_friend(self):
        dg = add_friend_Dialog.add_friend_Dialog()
        answer = dg.exec()
        if answer > 0:
            item = QListWidgetItem()
            name = dg.nameEdit.text()
            answer = CS.query_state(name)
            if answer == 'Incorrect No.' or answer == 'Please send the correct message.':
                QMessageBox.warning(self, 'Warning', '该用户不存在')
                return
            iconpath = dg.get_iconpath()
            font = QFont()
            font.setPointSize(16)

            item.setText(name)
            item.setIcon(QIcon(iconpath))
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)

            self.addItem(item)




    def delete_friend(self):
        del_items = self.selectedItems()
        for item in del_items:
            self.takeItem(self.row(item))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SAO_ListWidget()
    sys.exit(app.exec_())



