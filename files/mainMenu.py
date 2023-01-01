import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QPushButton, QDialog, QApplication, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QSizePolicy, QMessageBox

from files.storage import storage
from files.table import barTable
from offlineDB.getFromOfflineDB import getDailyReport


def offsetWindow(offset):
    screen = QApplication.primaryScreen().size()
    width = screen.width()
    height = screen.height()

    x = math.floor(offset * width / 100)
    y = math.floor(offset * height / 100)
    w = math.floor(width - (x + x))
    h = math.floor(height - (y + y))
    return x, y, w, h


class mainMenu(QDialog):
    def __init__(self):
        super().__init__()

        self.startX, self.startY, self.startW, self.startH = offsetWindow(20)
        self.setGeometry(self.startX, self.startY, self.startW, self.startH)
        self.setMinimumSize(self.startW, self.startH)
        self.setMaximumSize(self.startW, self.startH)
        self.setWindowTitle("Bar")
        self.myLayout = QVBoxLayout()
        self.setAcceptDrops(True)
        self.storageTab = None

        self.gboxButtons, self.gboxButtonsLayout = self.createHLayout()
        self.gboxBar, self.gboxBarLayout = self.createHLayout()
        self.gboxAddTable, self.gboxAddTableLayout = self.createHLayout()

        self.gboxBar.setStyleSheet(""" QGroupBox {
            border-image: url(images/bar_background.png);
        }""")
        self.gboxAddTable.setStyleSheet(""" QGroupBox {
            background-color: black;
        }
        Button {
            position: relative;
            background-color: #4CAF50;
            border: none;
            font-size: 28px;
            color: #FFFFFF;
            padding: 20px;
            width: 200px;
            text-align: center;
            transition-duration: 0.4s;
            text-decoration: none;
            overflow: hidden;
            cursor: pointer;
        } 
        Button:after {
            content: "";
            background: #f1f1f1;
            display: block;
            position: absolute;
            padding-top: 300%;
            padding-left: 350%;
            margin-left: -20px !important;
            margin-top: -120%;
            opacity: 0;
            transition: all 0.8s
        }
        Button:active:after {
            padding: 0;
            margin: 0;
            opacity: 1;
            transition: 0s
        }""")
        self.gboxButtons.setStyleSheet(""" QGroupBox {
            background-color: black;
        } 
        Button {
            display: inline-block;
            padding: 15px 25px;
            font-size: 24px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            outline: none;
            color: #fff;
            background-color: #4CAF50;
            border: none;
            border-radius: 15px;
            box-shadow: 0 9px #999;
        }
        Button:hover {background-color: #3e8e41}

        """)

        self.populateButtonsLayout("STORAGE", self.gboxButtonsLayout, self.handleCallbacks)
        self.populateButtonsLayout("DAILY REPORT", self.gboxButtonsLayout, self.handleCallbacks)

        self.populateButtonsLayout("ADD TABLE", self.gboxAddTableLayout, self.handleCallbacks)

        self.myLayout.addWidget(self.gboxButtons, 1)
        self.myLayout.addWidget(self.gboxBar, 8)
        self.myLayout.addWidget(self.gboxAddTable, 1)

        self.setLayout(self.myLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.show()

    def createHLayout(self):
        gbox = QGroupBox()
        gboxLayout = QHBoxLayout()
        gbox.setLayout(gboxLayout)
        gboxLayout.setSpacing(0)
        gboxLayout.setContentsMargins(0, 0, 0, 0)
        return gbox, gboxLayout

    def populateButtonsLayout(self, name, layout, callback=None):
        btn = Button(name, callback)
        layout.addWidget(btn)

    def handleCallbacks(self, btnName):
        if btnName == "STORAGE":
            self.storageTab = storage()
        if btnName == "DAILY REPORT":
            msg = msgBox("Daily Report", f"""Daily Report: {getDailyReport()} din""", "I")
        if btnName == "ADD TABLE":
            barTable(self)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        offset = QPoint(30, 25)
        position = e.pos() - offset
        e.source().move(position)
        e.setDropAction(Qt.MoveAction)
        e.accept()


class Button(QPushButton):
    def __init__(self, name, callback):
        super().__init__()

        self.name = name
        self.callback = callback

        self.setText(name)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.callback(self.name)

    def closeEvent(self, e):
        print('closing')


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
