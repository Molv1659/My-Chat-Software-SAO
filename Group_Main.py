from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import Group_ListWidget
import CS
import P2P
from socket import *
import threading
import time
import os
import codecs
import json
import re

class Group_main(QWidget):
    #为了自己电脑上跑两个号，最终应该改成同一个端口，别忘了！
    PORT1 = 11113
    PORT2 = 11113
    all_msg_info = []
    top_group_info = []
    close_signal = pyqtSignal()
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.initUI()
        self.initData()
        self.receiver = P2P.Chat_Receiver(self.PORT1)
        self.receiver.rcv_msg.connect(self.deal_msg)
        self.receiver.start()
        self.groups_list.choose_group.connect(self.choose_chat)
        self.groups_list.initDATA(self.top_group_info, self.id)
        self.dst = ''


    def initData(self):
        self.top_group_info = []
        if  os.path.exists(self.id + '/' + 'groupinfo.json'):
            with codecs.open(self.id + '/' + 'groupinfo.json', 'r', 'utf-8') as f:
                for line in f:
                    dic = json.loads(line)
                    self.top_group_info.append(dic)
        else:
            with codecs.open(self.id + '/' + 'groupinfo.json', 'w', 'utf-8') as f:
                print('第一次登陆新建群聊信息')
        self.all_msg_info = []
        if  os.path.exists(self.id + '/' + 'all_group_msg_info.json'):
            with codecs.open(self.id + '/' + 'all_group_msg_info.json', 'r', 'utf-8') as f:
                for line in f:
                    dic = json.loads(line)
                    self.all_msg_info.append(dic)
        else:
            with codecs.open(self.id + '/' + 'all_group_msg_info.json', 'w', 'utf-8') as f:
                print('第一次登陆新建群聊聊天记录信息')


    def closeEvent(self, event):

        with codecs.open(self.id + '/' + 'groupinfo.json', 'w', 'utf-8') as f:
            for i in range(len(self.groups_list.group_info)):
                item = self.groups_list.group_info[i]
                group = {}
                group['group_name'] = item['group_name']
                group['member'] = item['member']
                json.dump(group, f, ensure_ascii=False)
                f.write('\r\n')

        with codecs.open(self.id + '/' + 'all_group_msg_info.json', 'w', 'utf-8') as f:
            for i in range(len(self.all_msg_info)):
                json.dump(self.all_msg_info[i], f, ensure_ascii=False)
                f.write('\r\n')

        self.receiver.end()
        self.close_signal.emit()


    def choose_chat(self, id):
        self.dst = id
        self.renew_chat_window()

    def renew_chat_window(self):
        self.chatwindow.setPlainText('chat in:' + self.dst + '\r\n')
        for i in range(len(self.all_msg_info)):
            data = self.all_msg_info[i]
            if data['group_info']['group_name'] == self.dst:
                self.chatwindow.appendPlainText(data['time'] + '  ' + data['src'] + ': \n\r' + data['data'] + '\n\r\n\r')


    def deal_msg(self,data):
        self.all_msg_info.append(data)
        if data['type']=='text':
            print('1')
        else:
            print('2')
            print(data['group_info']['group_name'])
        have = self.groups_list.have_this_group(data['group_info']['group_name'])
        if data['type']=='text':
            print('11')
        else:
            print('22')
        if not have:
            self.groups_list.add_unknown_group(data['group_info']['group_name'], data['group_info']['member'])
        if data['type']=='text':
            print('111')
        else:
            print('222')


    def initUI(self):
        self.btn1 = QPushButton('发送',self)
        self.btn1.clicked.connect(self.send_msg)
        self.btn2 = QPushButton('清空', self)
        self.btn2.clicked.connect(self.clearupsend)
        self.btn3 = QPushButton('发送文件', self)
        self.btn3.clicked.connect(self.send_file)
        self.btn4 = QPushButton('创建群聊', self)
        self.btn4.clicked.connect(self.create_groupchat)
        self.chatwindow = QPlainTextEdit(self)
        self.sendwindow = QPlainTextEdit(self)
        self.groups_list = Group_ListWidget.Group_ListWidget()


        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.groups_list, 1, 0, 7, 3)
        self.grid.addWidget(self.chatwindow, 1, 3, 4, 6)
        self.grid.addWidget(self.btn3, 5, 3, 1, 1)
        self.grid.addWidget(self.sendwindow, 6, 3, 2, 6)
        self.grid.addWidget(self.btn4, 8, 0, 1, 1)
        self.grid.addWidget(self.btn2, 8, 7, 1, 1)
        self.grid.addWidget(self.btn1, 8, 8, 1, 1)
        self.setLayout(self.grid)

        self.setWindowTitle('SAO-mail of ' + self.id)
        self.resize(1100,700)
        self.center()
        self.show()


    def create_groupchat(self):
        self.groups_list.add_group(self.id)


    def clearupsend(self):
        self.sendwindow.setPlainText('')

    def send_file(self):
        data = {}
        data['type'] = 'file'
        temp = {}
        temp['group_name'] = self.dst
        for i in range(len(self.groups_list.group_info)):
            groupname = self.groups_list.group_info[i]['group_name']
            if groupname == self.dst:
                temp['member'] = self.groups_list.group_info[i]['member']
        data['group_info'] = temp
        data['src'] = self.id
        filename = QFileDialog.getOpenFileName(self, '打开文件', './res/')
        if filename[0]:
            the_filename = filename[0]
            print('打开了'+the_filename)
        else:
            return
        data['data'] = os.path.basename(the_filename)
        data['time'] = time.asctime(time.localtime(time.time()))
        self.all_msg_info.append(data)

        for i in range(len(self.groups_list.group_info)):
            groupname = self.groups_list.group_info[i]['group_name']
            if groupname == self.dst:
                IDs = self.groups_list.group_info[i]['member']
                for j in range(len(IDs)):
                    if self.id!=IDs[j]:
                        P2P.send_group_file(self.groups_list.group_info[i], self.id, IDs[j], self.PORT2, the_filename)

        self.renew_chat_window()

    def send_msg(self):
        msg = self.sendwindow.toPlainText()
        if msg == '':
            QMessageBox.warning(self,'Warning','发送消息不可为空', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        data = {}
        data['type'] = 'text'
        data['src'] = self.id
        temp = {}
        temp['group_name'] = self.dst
        for i in range(len(self.groups_list.group_info)):
            groupname = self.groups_list.group_info[i]['group_name']
            if groupname == self.dst:
                temp['member'] = self.groups_list.group_info[i]['member']
        data['group_info'] = temp
        data['data'] = msg
        data['time'] = time.asctime(time.localtime(time.time()))
        self.all_msg_info.append(data)

        for i in range(len(self.groups_list.group_info)):
            groupname = self.groups_list.group_info[i]['group_name']
            if groupname == self.dst:
                IDs = self.groups_list.group_info[i]['member']
                for j in range(len(IDs)):
                    if self.id!=IDs[j]:
                        P2P.send_group_msg(self.groups_list.group_info[i], self.id, IDs[j], self.PORT2, msg)
        self.sendwindow.setPlainText('')
        self.renew_chat_window()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Group_main('2017011534')
    sys.exit(app.exec_())