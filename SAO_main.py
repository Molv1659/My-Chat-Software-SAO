from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import SAO_ListWidget
import Group_Main
import CS
import P2P
from socket import *
import threading
import time
import os
import codecs
import json
import re

class SAO_main(QWidget):
    #为了自己电脑上跑两个号，最终应该改成同一个端口，别忘了！
    PORT1 = 11111
    PORT2 = 11111
    group_chat = 0
    all_msg_info = []
    friend_info = []
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.initUI()
        self.initData()
        self.receiver = P2P.Chat_Receiver(self.PORT1)
        self.receiver.rcv_msg.connect(self.deal_msg)
        self.receiver.start()
        self.friends_list.choose_friend.connect(self.choose_chat)
        self.friends_list.initDATA(self.friend_info, self.id)
        self.dst = ''


    def initData(self):
        if not os.path.exists(self.id+'/'):
            os.makedirs(self.id+'/')
        if  os.path.exists(self.id + '/' + 'friendinfo.json'):
            with codecs.open(self.id + '/' + 'friendinfo.json', 'r', 'utf-8') as f:
                for line in f:
                    dic = json.loads(line)
                    self.friend_info.append(dic)
        else:
            with codecs.open(self.id + '/' + 'friendinfo.json', 'w', 'utf-8') as f:
                print('第一次登陆新建好友信息')

        if  os.path.exists(self.id + '/' + 'all_msg_info.json'):
            with codecs.open(self.id + '/' + 'all_msg_info.json', 'r', 'utf-8') as f:
                for line in f:
                    dic = json.loads(line)
                    self.all_msg_info.append(dic)
        else:
            with codecs.open(self.id + '/' + 'all_msg_info.json', 'w', 'utf-8') as f:
                print('第一次登陆新建聊天记录信息')







    def choose_chat(self, id):
        self.dst = id
        self.renew_chat_window()

    def renew_chat_window(self):
        self.chatwindow.setPlainText('chat with:' + self.dst + '\r\n')
        for i in range(len(self.all_msg_info)):
            data = self.all_msg_info[i]
            if data['src'] ==self.dst:
                self.chatwindow.appendPlainText(data['time'] + '  ' + data['src'] + ': \n\r' + data['data'] + '\n\r\n\r')
            elif data['dst'] == self.dst:
                self.chatwindow.appendPlainText(data['time'] + '  ' + data['src'] + ': \n\r' + data['data'] + '\n\r\n\r')


    def deal_msg(self,data):
        self.all_msg_info.append(data)
        have = self.friends_list.have_this_friend(data['src'])
        if not have:
            self.friends_list.add_unknown_friend(data['src'])
        #收消息后在那个人的名字text那儿加个*，双击点进去后*消失
        self.friends_list.un_rcv_label(data['src'])

    def initUI(self):
        self.btn1 = QPushButton('发送',self)
        self.btn1.clicked.connect(self.send_msg)
        self.btn2 = QPushButton('清空', self)
        self.btn2.clicked.connect(self.clearupsend)
        self.btn3 = QPushButton('发送文件', self)
        self.btn3.clicked.connect(self.send_file)
        self.btn4 = QPushButton('群聊', self)
        self.btn4.clicked.connect(self.groupchat)
        self.btn5 = QPushButton('添加好友', self)
        self.btn5.clicked.connect(self.add_friend)
        self.chatwindow = QPlainTextEdit(self)
        self.sendwindow = QPlainTextEdit(self)
        self.friends_list = SAO_ListWidget.SAO_ListWidget()


        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.friends_list, 1, 0, 7, 3)
        self.grid.addWidget(self.chatwindow, 1, 3, 4, 6)
        self.grid.addWidget(self.btn3, 5, 3, 1, 1)
        self.grid.addWidget(self.sendwindow, 6, 3, 2, 6)
        self.grid.addWidget(self.btn5, 8, 1, 1, 1)
        self.grid.addWidget(self.btn4, 8, 3, 1, 1)
        self.grid.addWidget(self.btn2, 8, 7, 1, 1)
        self.grid.addWidget(self.btn1, 8, 8, 1, 1)
        self.setLayout(self.grid)

        self.setWindowTitle('SAO-mail of ' + self.id)
        self.resize(1100,700)
        self.center()
        self.show()

    def add_friend(self):
        self.friends_list.add_friend()


    def groupchat(self):
        if self.group_chat == 0:
            self.groupchatwindow = Group_Main.Group_main(self.id)
            self.group_chat = 1
            self.groupchatwindow.close_signal.connect(self.closegroup)
        else:
            return

    def closegroup(self):
        self.group_chat = 0;




    def clearupsend(self):
        self.sendwindow.setPlainText('')

    def send_file(self):
        data = {}
        data['type'] = 'file'
        data['src'] = self.id
        data['dst'] = self.dst
        filename = QFileDialog.getOpenFileName(self, '打开文件', './res/')
        if filename[0]:
            the_filename = filename[0]
            print('打开了'+the_filename)
        else:
            return
        data['data'] = os.path.basename(the_filename)
        data['time'] = time.asctime(time.localtime(time.time()))
        self.all_msg_info.append(data)
        P2P.send_file(self.id, self.dst, self.PORT2, the_filename)
        self.renew_chat_window()



    def send_msg(self):
        msg = self.sendwindow.toPlainText()
        if msg == '':
            QMessageBox.warning(self,'Warning','发送消息不可为空', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        data = {}
        data['type'] = 'text'
        data['src'] = self.id
        data['dst'] = self.dst
        data['data'] = msg
        data['time'] = time.asctime(time.localtime(time.time()))
        self.all_msg_info.append(data)
        P2P.send_msg(self.id, self.dst, self.PORT2, msg)
        self.sendwindow.setPlainText('')
        self.renew_chat_window()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '退出', "是否要退出该账号？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            with codecs.open(self.id+'/'+'friendinfo.json', 'w', 'utf-8') as f:
                for i in range(self.friends_list.count()):
                    item = self.friends_list.item(i)
                    id = re.findall(r'\d{10}', item.text())[0]
                    friend = {}
                    friend['id'] = id
                    json.dump(friend, f, ensure_ascii=False)
                    f.write('\r\n')

            with codecs.open(self.id+'/'+'all_msg_info.json', 'w', 'utf-8') as f:
                for i in range(len(self.all_msg_info)):
                    json.dump(self.all_msg_info[i], f, ensure_ascii=False)
                    f.write('\r\n')


            CS.logout(self.id)
            print('将要关线程')
            self.receiver.end()
            self.friends_list.end()
            time.sleep(0.3)
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = SAO_main('2017011534')
    sys.exit(app.exec_())