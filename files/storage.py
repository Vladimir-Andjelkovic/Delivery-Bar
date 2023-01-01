import math

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QDialog, QFormLayout, QPushButton, QVBoxLayout, QGridLayout, QWidget, QLabel, QComboBox,\
    QMessageBox, QGroupBox, QApplication, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QLineEdit
from offlineDB.getFromOfflineDB import searchPartialItem, getItemsFromCategory
from offlineDB.addDelToOfflineDB import addItemToOffDB, deleteFromOffDB


def offsetWindow(offset):
    screen = QApplication.primaryScreen().size()
    width = screen.width()
    height = screen.height()

    x = math.floor(offset * width / 100)
    y = math.floor(offset * height / 100)
    w = math.floor(width - (x + x))
    h = math.floor(height - (y + y))
    return x, y, w, h


class storage(QDialog):
    def __init__(self):
        super().__init__()

        self.win = QDialog()
        self.startX, self.startY, self.startW, self.startH = offsetWindow(15)
        self.setGeometry(self.startX, self.startY, self.startW, self.startH)
        self.setMinimumSize(400, 400)
        self.setWindowTitle('MAGACIN')
        self.myLayout = QVBoxLayout()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.storageTable = None
        self.searchBar = None
        self.addWindow = None

        self.gboxStorageButtons, self.storageButtonsLayout = self.createGridLayout()
        self.gboxTableView, self.tableViewLayout = self.createGridLayout()

        self.myLayout.addWidget(self.gboxStorageButtons, 2)
        self.myLayout.addWidget(self.gboxTableView, 8)

        self.populateTable(self.tableViewLayout)
        self.populateStorageButtons(self.storageButtonsLayout, self.toolsCallback)

        self.setStyleSheet(""" QDialog {
                    border-image: url(images/drinks.jpg);
                }""")

        self.setLayout(self.myLayout)
        self.show()

    def createGridLayout(self):
        gbox = QGroupBox()
        gboxLayout = QGridLayout()
        gbox.setLayout(gboxLayout)
        gbox.setStyleSheet("""QGroupBox {
                    border: none;
                }""")

        return gbox, gboxLayout

    def populateTable(self, layout, table=None, search=None):

        if table is not None:
            table.deleteLater()
            self.storageTable = None

        if search is None:
            itemsInfo = getItemsFromCategory()
        else:
            itemsInfo = searchPartialItem(search)

        columnCount = 4
        rowCount = len(itemsInfo)

        columnNames = ['NAME', 'QUANTITY', 'PRICE', 'TYPE']
        table = QTableWidget()
        table.setColumnCount(columnCount)
        table.setHorizontalHeaderLabels(columnNames)
        table.setRowCount(rowCount)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # makes columns fit into table
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        row = -1
        for i in itemsInfo:
            c = 0
            row += 1
            for y in i:
                table.setItem(row, c, QTableWidgetItem(str(y)))
                c += 1

        table.setStyleSheet("""QTableWidget {
                    background-color: rgb(255, 255, 255, 0.8);
                }""")

        layout.addWidget(table)
        self.storageTable = table

    def populateStorageButtons(self, layout, callback=None):
        lblStorage = QLabel('STORAGE')
        lblStorage.setFont(QFont('Arial', 30))

        searchBar = QLineEdit()
        searchBar.setFixedHeight(40)
        font = searchBar.font()
        font.setPointSize(16)
        searchBar.setFont(font)

        toolsNames = ["ADD", "DELETE", "PRINT", "SEARCH", "RESET", "REFRESH"]
        tools = []
        for i in toolsNames: tools.append(storageTools(i, callback))

        layout.addWidget(lblStorage, 0, 0)
        layout.addWidget(tools[0], 0, 4)
        layout.addWidget(tools[1], 0, 5)
        layout.addWidget(tools[2], 0, 6)
        layout.addWidget(searchBar, 1, 0)
        layout.addWidget(tools[3], 1, 1)
        layout.addWidget(tools[4], 1, 2)
        layout.addWidget(tools[5], 1, 6)

        lblStorage.setFont(QFont('Arial', 30))
        lblStorage.setStyleSheet("""QLabel {
            color: #1DD7C1
        }""")

        searchBar.returnPressed.connect(lambda: [self.toolsCallback("SEARCH")])

        self.searchBar = searchBar

    def addItemToStorage(self):
        addDialog = QDialog()
        addDialog.setWindowTitle("Add Item")
        addDialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        x, y, w, h = offsetWindow(31)
        addDialog.setGeometry(x, y, w, h)
        addDialog.setMinimumSize(w, h)
        addDialog.setMaximumSize(w, h)

        formLayout = QFormLayout()

        lblName = addLabels("ITEM NAME:")
        lblQuantity = addLabels("ITEM QUANTITY:")
        lblPrice = addLabels("ITEM PRICE:")
        lblType = addLabels("ITEM TYPE:")

        leName = addLineEdit()
        leQuantity = addLineEdit()
        lePrice = addLineEdit()

        onlyInt = QIntValidator()
        leQuantity.setValidator(onlyInt)
        lePrice.setValidator(onlyInt)

        cbType = QComboBox()
        cbType.setMinimumHeight(60)
        cbType.setFont(QFont('Ariel', 10))
        cbItems = ["SOKOVI", "VODA", "ENERGETSKI NAPICI", "KAFE", "PIVO", "VISKI", "VINA", "DOMACE RAKIJE",
                   "STRANA ZESTOKA PICA", "KONJAK"]
        for i in cbItems:
            cbType.addItem(i)

        addButton = addItemButton('ADD', leName, leQuantity, lePrice, cbType, self.addToDatabaseCallback)
        addButton.setMinimumHeight(60)
        addButton.setFont(QFont('Ariel', 16))

        spaceWidget = QWidget()
        spaceWidget.setMinimumHeight(30)

        formLayout.addRow(lblName, leName)
        formLayout.addRow(lblQuantity, leQuantity)
        formLayout.addRow(lblPrice, lePrice)
        formLayout.addRow(lblType, cbType)
        formLayout.addWidget(spaceWidget)
        formLayout.addWidget(addButton)

        addDialog.setLayout(formLayout)
        addDialog.show()
        return addDialog

    def toolsCallback(self, btnName):
        if btnName == "SEARCH":
            search = self.searchBar.text()
            self.populateTable(self.tableViewLayout, self.storageTable, search)

        if btnName == "RESET":
            self.searchBar.setText('')
            self.populateTable(self.tableViewLayout, self.storageTable, '')

        if btnName == "ADD":
            self.addWindow = self.addItemToStorage()

        if btnName == "DELETE":
            self.deleteRowFromDatabase()

        if btnName == "REFRESH":
            self.searchBar.setText('')
            self.populateTable(self.tableViewLayout, self.storageTable, '')

        if btnName == "PRINT":
            msg = msgBox("Error!", "You don't have authorization to do this.", "W")

    def addToDatabaseCallback(self, itemName, itemQuantity, itemPrice, cbText):

        itemNam = itemName.upper()

        i = addItemToOffDB(itemNam, itemQuantity, itemPrice, cbText)

        if i == 0:
            msg = msgBox("Success!", "Successfully added item to the database.", "I")
            self.searchBar.setText('')
            self.populateTable(self.tableViewLayout, self.storageTable, '')
        elif i == -1:
            msg = msgBox("Error!", "That item already exists.", "W")

    def deleteRowFromDatabase(self):
        selectedRowIndex = self.storageTable.currentRow()
        if selectedRowIndex > -1:
            itemName = self.storageTable.item(selectedRowIndex, 0).text()
            category = self.storageTable.item(selectedRowIndex, 3).text()

            deleteFromOffDB(itemName, category)

            self.populateTable(self.tableViewLayout, self.storageTable, '')

        else:
            msg = msgBox("Error!", "Nothing is selected.", "W")


class storageTools(QPushButton):
    def __init__(self, btnName, callback):
        super().__init__()

        self.name = btnName
        self.callback = callback

        self.setFixedHeight(50)
        self.setFixedWidth(100)
        self.setText(self.name)

        if btnName == "DELETE":
            self.setStyleSheet("""QPushButton {           
                                display: inline-block;
                                outline: none;
                                cursor: pointer;
                                font-size: 14px;
                                line-height: 1;
                                border-radius: 500px;
                                transition-property: background-color,border-color,color,box-shadow,filter;
                                transition-duration: .3s;
                                border: 1px solid transparent;
                                letter-spacing: 2px;
                                min-width: 100px;
                                text-transform: uppercase;
                                white-space: normal;
                                font-weight: 700;
                                text-align: center;
                                padding: 17px 48px;
                                color: #fff;
                                background-color: #1ED760;
                                height: 48px;
                            }
                            QPushButton:hover {    
                                transform: scale(1.04);
                                background-color: red;
                            }""")
        else:
            self.setStyleSheet("""QPushButton {           
                                display: inline-block;
                                outline: none;
                                cursor: pointer;
                                font-size: 14px;
                                line-height: 1;
                                border-radius: 500px;
                                transition-property: background-color,border-color,color,box-shadow,filter;
                                transition-duration: .3s;
                                border: 1px solid transparent;
                                letter-spacing: 2px;
                                min-width: 100px;
                                text-transform: uppercase;
                                white-space: normal;
                                font-weight: 700;
                                text-align: center;
                                padding: 17px 48px;
                                color: #fff;
                                background-color: #1ED760;
                                height: 48px;
                            }
                            QPushButton:hover {    
                                transform: scale(1.04);
                                background-color: #21e065;
                            }""")


    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.callback(self.name)


class addLabels(QLabel):
    def __init__(self, name):
        super().__init__()

        self.setText(name)
        self.setMinimumHeight(60)
        self.setFont(QFont('Ariel', 13))


class addLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(60)
        self.setFont(QFont('Ariel', 13))


class addItemButton(QPushButton):
    def __init__(self, btnName, itemName, itemQuantity, itemPrice, cbText, callback):
        super().__init__()

        self.itemName = itemName
        self.itemQuantity = itemQuantity
        self.itemPrice = itemPrice
        self.cbText = cbText
        self.callback = callback

        self.setText(btnName)

    def mousePressEvent(self, e):
        if self.itemName.text() and self.itemQuantity.text() and self.itemPrice.text():
            self.callback(self.itemName.text(), self.itemQuantity.text(), self.itemPrice.text(),
                          self.cbText.currentText())
        else:
            print('Error: something was typed wrong')


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
