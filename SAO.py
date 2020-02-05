from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import SAO_login
import SAO_main


class SAO():
    def __init__(self):
        self.loginWindow = SAO_login.SAO_login()
        self.loginWindow.login_signal.connect(self.login)

    def login(self, id):
        self.mainWindow = SAO_main.SAO_main(id)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = SAO()
    sys.exit(app.exec_())