from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class add_friend_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.icon_default = True
        self.iconpath = './res/default.jpg'

    def initUI(self):

        self.setWindowIcon(QIcon('./res/SAO.png'))

        self.label1 = QLabel('好友昵称：', self)
        self.label2 = QLabel('好友头像:', self)
        self.nameEdit = QLineEdit(self)
        self.btn1 = QPushButton('浏览', self)
        self.btn1.setEnabled(False)
        self.btn2 = QPushButton('确认', self)
        self.btn3 = QPushButton('取消', self)
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


        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label1, 1, 0)
        self.grid.addWidget(self.nameEdit, 1, 1)
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



    def unack(self):
        self.done(-1)


    def ack(self):
        if len(self.nameEdit.text()) != 0:
            self.done(1)
        else:
            QMessageBox.information(self, 'Warning', '未输入好友姓名')


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
    ex = add_friend_Dialog()
    sys.exit(app.exec_())
