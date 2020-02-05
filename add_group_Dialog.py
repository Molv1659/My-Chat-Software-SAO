from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import CS

class add_group_Dialog(QDialog):
    group_name = ''
    member = []

    def __init__(self):
        super().__init__()
        self.initUI()
        self.icon_default = True
        self.iconpath = './res/group.jpg'

    def initUI(self):

        self.setWindowIcon(QIcon('./res/SAO.png'))

        self.label1 = QLabel('组员账号：', self)
        self.label2 = QLabel('群头像:', self)
        self.label3 = QLabel('群名：', self)
        self.nameEdit = QLineEdit(self)
        self.groupEdit = QLineEdit(self)
        self.btn1 = QPushButton('浏览', self)
        self.btn1.setEnabled(False)
        self.btn2 = QPushButton('确认', self)
        self.btn3 = QPushButton('取消', self)
        self.btn4 = QPushButton('添加该组员', self)

        self.rbtn1 = QRadioButton('默认', self)
        self.rbtn1.setChecked(True)
        self.rbtn2 = QRadioButton('本地选择', self)
        self.bg = QButtonGroup(self)
        self.bg.addButton(self.rbtn1, 1)
        self.bg.addButton(self.rbtn2, 2)

        self.bg.buttonClicked.connect(self.rbclicked)
        self.btn1.clicked.connect(self.browse_icon)
        self.btn2.clicked.connect(self.ack)
        self.btn3.clicked.connect(self.unack)
        self.btn4.clicked.connect(self.add_member)


        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label3, 0, 0)
        self.grid.addWidget(self.groupEdit, 0, 1)
        self.grid.addWidget(self.label1, 1, 0)
        self.grid.addWidget(self.nameEdit, 1, 1)
        self.grid.addWidget(self.btn4, 1, 2)
        self.grid.addWidget(self.label2, 2, 0)
        self.grid.addWidget(self.rbtn1, 3, 0)
        self.grid.addWidget(self.rbtn2, 3, 1)
        self.grid.addWidget(self.btn1, 3, 2)
        self.grid.addWidget(self.btn2, 4, 0)
        self.grid.addWidget(self.btn3, 4, 1)


        self.setLayout(self.grid)
        self.resize(300, 120)
        self.center()
        self.setWindowTitle('Add Friend')
        self.show()


    def add_member(self):
        name = self.nameEdit.text()
        answer = CS.query_state(name)
        if answer == 'Incorrect No.' or answer == 'Please send the correct message.':
            QMessageBox.warning(self, 'Warning', '该用户不存在')
            return
        else:
            for i in range(len(self.member)):
                if self.member[i] == name:
                    QMessageBox.warning(self, 'Warning', '已添加该用户')
                    return
            self.member.append(name)
            QMessageBox.information(self, 'OK', '成功添加')
            self.nameEdit.setText('')

    def unack(self):
        self.done(-1)


    def ack(self):
        if len(self.member) != 0 and self.groupEdit.text()!= '':
            self.group_name = self.groupEdit.text()
            self.done(1)
        else:
            QMessageBox.information(self, 'Warning', '未添加任何组员或没有输入群名')


    def browse_icon(self):
        filename = QFileDialog.getOpenFileName(self, '打开文件', './res/')
        if filename[0]:
            self.iconpath = filename[0]


    def rbclicked(self):
        if self.bg.checkedId() == 1:
            self.btn1.setEnabled(False)
        else:
            self.icon_default = False
            self.btn1.setEnabled(True)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def get_iconpath(self):
        return self.iconpath

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = add_group_Dialog()
    sys.exit(app.exec_())
