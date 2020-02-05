import sys
import CS
import P2P
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SAO_login(QWidget):

    login_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.label1 = QLabel('Please enter your ID:', self)
        self.label2 = QLabel('Please enter your password:', self)

        self.btn1 = QPushButton("Sign In", self)
        self.btn1.clicked.connect(self.login)

        self.btn2 = QPushButton("Quit", self)
        self.btn2.clicked.connect(QCoreApplication.instance().quit)

        self.idEdit = QLineEdit(self)
        self.idEdit.setPlaceholderText('your ID')
        self.passwordEdit = QLineEdit(self)
        self.passwordEdit.setPlaceholderText('your passport')
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label1, 1, 0, 1, 2)
        self.grid.addWidget(self.idEdit, 2, 0, 1, 2)
        self.grid.addWidget(self.label2, 3, 0, 1, 2)
        self.grid.addWidget(self.passwordEdit, 4, 0, 1, 2)
        self.grid.addWidget(self.btn1, 5, 0, 2, 1)
        self.grid.addWidget(self.btn2, 5, 1, 2, 1)
        self.setLayout(self.grid)

        self.setWindowIcon(QIcon('./res/SAO.png'))
        self.resize(300,200)
        self.center()
        self.setWindowTitle('login window')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def login(self):
        id = self.idEdit.text()

        if CS.login(id):
            self.login_signal.emit(id)
            self.close()
        else:
            QMessageBox.warning(self,'WARNING!', 'Your id or passport is wrong!')


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = SAO_login()
    sys.exit(app.exec_())