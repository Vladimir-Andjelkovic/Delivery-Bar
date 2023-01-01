from PyQt5 import Qt
import math
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QApplication, QFormLayout, QPushButton, QLabel, QLineEdit, QVBoxLayout, QMessageBox

from files.mainMenu import mainMenu
from offlineDB.getFromOfflineDB import getLoginInfo
import math


def offsetWindow(offset):
    screen = QApplication.primaryScreen().size()
    width = screen.width()
    height = screen.height()

    x = math.floor(offset * width / 100)
    y = math.floor(offset * height / 100)
    w = math.floor(width - (x + x))
    h = math.floor(height - (y + y))
    return x, y, w, h


class loginScreen(QDialog):
    def __init__(self):
        super().__init__()

        self.startX, self.startY, self.startW, self.startH = offsetWindow(33)
        self.setGeometry(self.startX, self.startY, self.startW, self.startH)
        self.setMinimumSize(self.startW, self.startH)
        self.setMaximumSize(self.startW, self.startH)
        self.setWindowTitle("Welcome")
        self.myLayout = QVBoxLayout()

        self.lblLoginLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.btnLoginLayout = QVBoxLayout()

        self.populateLabelLayout(self.lblLoginLayout)
        self.username, self.password = self.populateFormLayout(self.formLayout)
        self.btnLogin = self.populateBtnLayout(self.btnLoginLayout)

        self.btnLogin.clicked.connect(self.checkLogin)

        self.myLayout.addLayout(self.lblLoginLayout)
        self.myLayout.addLayout(self.formLayout)
        self.myLayout.addLayout(self.btnLoginLayout)

        self.setStyleSheet("""QDialog {
            color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));
            background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 cyan, stop:1 blue);}");
        }""")

        self.setLayout(self.myLayout)
        self.show()

    def populateLabelLayout(self, layout):
        lbl = QLabel('LOGIN')
        lbl.setAlignment(Qt.Qt.AlignCenter)
        lbl.setFont(QFont("Arial", 30))


        layout.addWidget(lbl)

    def populateFormLayout(self, layout):
        lblUser = QLabel("USERNAME:")
        lblPass = QLabel("PASSWORD:")
        leUser = QLineEdit()
        lePass = QLineEdit()

        lblUser.setFont(QFont("Arial", 17))
        lblPass.setFont(QFont("Arial", 17))

        leUser.setFixedHeight(40)
        lePass.setFixedHeight(40)
        leUser.setFont(QFont("Arial", 17))
        lePass.setFont(QFont("Arial", 17))
        leUser.setStyleSheet("""QLineEdit {
                    background: transparent;
                }""")
        lePass.setStyleSheet("""QLineEdit {
                    background: transparent;
                }""")

        lePass.setEchoMode(QLineEdit.Password)

        layout.addRow(lblUser, leUser)
        layout.addRow(lblPass, lePass)

        return leUser, lePass

    def populateBtnLayout(self, layout):
        btn = QPushButton("LOGIN")
        btn.setFixedSize(self.startW - 150, 70)

        btn.setStyleSheet(""" QPushButton {
            appearance: none;
            background: none;
            border: none;
            outline: none;
            cursor: pointer;

            padding: 5px 10px;
            border-radius: 8px;
            font-size: 28px;
            font-weight: 600;
            transition: 0.4s;

            color: #FFF;
            background-color: #68A0DE;
            transition: 0.1s;
            text-shadow: 0px 3px rgba(0,0,0,0.2);
        } QPushButton:hover {
            background-color: green;
        }""")

        layout.addWidget(btn, alignment=Qt.Qt.AlignCenter)

        return btn

    def checkLogin(self):
        username = self.username.text()
        password = self.password.text()

        if len(username) == 0 or len(password) == 0:
            msg = msgBox("Error", "Please fill in all the fields.", "C")
        else:
            tempList = getLoginInfo(username, password)
            if len(tempList) == 1:
                mainMenu()
                self.close()
            else:
                msg = msgBox("Error", "Username or password incorrect.", "C")


class msgBox(QMessageBox):
    def __init__(self, title, text, icon):
        super().__init__()
        # Critical, Warning, Information, Question
        self.setWindowTitle(title)
        self.setText(text)

        if icon == 'C':
            self.setIcon(QMessageBox.Critical)
        elif icon == 'W':
            self.setIcon(QMessageBox.Warning)
        elif icon == 'I':
            self.setIcon(QMessageBox.Information)
        elif icon == 'Q':
            self.setIcon(QMessageBox.Question)

        self.exec_()
