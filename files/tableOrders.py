import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QFormLayout, QPushButton, QScrollArea, QVBoxLayout, QGridLayout, QWidget, QLabel, \
     QHBoxLayout, QGroupBox, QApplication, QMessageBox
from hf import splitString
from offlineDB.getFromOfflineDB import getAllItemNames, getItemCategory, getItemNamesFromCategory, getItemInfo
from offlineDB.addDelToOfflineDB import addOrderToDailyReport, removeFromStorage


class orderDef(QDialog):

    def __init__(self, winTitle, win):
        super().__init__()
        self.parentWin = win
        self.title = winTitle
        self.orders = []
        self.categoryList = getItemCategory()
        self.itemPositions = []
        self.total = ordersTotal(0)

        # Window settings
        winGeometry = self.offsetWindow(10)
        x = winGeometry[0]
        y = winGeometry[1]
        w = winGeometry[2]
        h = winGeometry[3]
        self.setGeometry(x, y, w, h)
        self.setMinimumSize(w, h)
        self.setWindowTitle(self.title)

        self.myLayout = QHBoxLayout()

        # Creating layouts
        self.categoryLayout, self.gboxCategories = self.createVLayout('CATEGORIES')
        self.scrollItemsLayout, self.gboxItems = self.createVLayoutScroll('ITEMS')
        self.scrollOrdersLayout, self.gboxOrders = self.createFormLayoutScroll('ORDERS', self.total)

        self.myLayout.addWidget(self.gboxCategories)
        self.myLayout.addWidget(self.gboxItems)
        self.myLayout.addWidget(self.gboxOrders)

        # Populate layouts
        self.populateLayout(self.categoryList, self.categoryLayout, callback=self.mousecallbacks)
        self.populateGridLayout([], self.itemPositions, self.scrollItemsLayout, callback=self.mousecallbacks)
        self.populateLayout([], self.scrollOrdersLayout, callback=self.mousecallbacks)

        self.setStyleSheet("""QDialog {
            border-image: url(images/bar.jpg);
        }""")

        self.setLayout(self.myLayout)
        self.show()

    def offsetWindow(self, offset):
        screen = QApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()

        x = math.floor(offset * width / 100)
        y = math.floor(offset * height / 100)
        w = math.floor(width - (x + x))
        h = math.floor(height - (y + y))
        return x, y, w, h

    def createVLayout(self, name):
        gbox = QGroupBox(name)
        gboxLayout = QVBoxLayout()
        gbox.setLayout(gboxLayout)

        gbox.setStyleSheet("""QWidget {
            background: transparent;
        }QPushButton {
            display: inline-block;
            outline: 0;
            border: none;
            cursor: pointer;
            font-weight: 600;
            border-radius: 4px;
            font-size: 13px;
            height: 30px;
            background-color: #9147ff;
            color: white;
            padding: 0 10px;
        }QPushButton:hover {
            background-color: #772ce8;
        }""")
        return gboxLayout, gbox

    def createVLayoutScroll(self, name):
        gbox = QGroupBox(name)
        gboxLayout = QVBoxLayout()
        scroll = QScrollArea()
        scrollLayout = QGridLayout()
        widget = QWidget()
        scroll.setWidgetResizable(True)

        gbox.setStyleSheet("""QWidget {
            background: transparent;
        }QPushButton {
            display: inline-block;
            outline: 0;
            border: 0;
            cursor: pointer;
            background-color:  #4299e1;
            border-radius: 4px;
            font-size: 14px;
            border-bottom: 4px solid #2b6cb0;
            font-weight: 700;
            color: white;
            line-height: 26px;
        }QScrollArea {
            border: none;
        }""")

        widget.setLayout(scrollLayout)
        scroll.setWidget(widget)
        gboxLayout.addWidget(scroll)
        gbox.setLayout(gboxLayout)
        return scrollLayout, gbox

    def createFormLayoutScroll(self, name, btnTotal):
        gbox = QGroupBox(name)
        gboxLayout = QVBoxLayout()
        scroll = QScrollArea()
        scrollLayout = QFormLayout()
        widget = QWidget()
        scroll.setWidgetResizable(True)
        payBtn = payButton('PAY', self.payOrder)

        gbox.setStyleSheet("""QWidget {
            background-color: rgb(255, 255, 255, 0.5);
        }QLabel {
            background: transparent;
        }QPushButton {
            background: white;
        }""")

        widget.setLayout(scrollLayout)
        scroll.setWidget(widget)
        gboxLayout.addWidget(scroll)
        gbox.setLayout(gboxLayout)
        gboxLayout.addWidget(btnTotal)
        gboxLayout.addWidget(payBtn)
        return scrollLayout, gbox

    def populateLayout(self, items, layout, callback=None):
        while True:
            item = layout.takeAt(0)
            if item:
                if item.widget():
                    item.widget().deleteLater()
            else:
                break

        for i in items:
            btn = categoryButton(i, callback)
            btn.setFixedSize(160, 40)
            layout.addWidget(btn)

    def populateGridLayout(self, items, positions, layout, callback=None):
        while True:
            item = layout.takeAt(0)
            if item:
                if item.widget():
                    item.widget().deleteLater()
            else:
                break

        for position, item in zip(positions, items):
            btn = itemButton(item, callback)
            btn.setFixedSize(150, 80)
            layout.addWidget(btn, *position)

    def mousecallbacks(self, name):
        for i in self.categoryList:
            if name == i:
                columns = 3
                rows = math.ceil(len(getItemNamesFromCategory(name)) / columns)
                positions = [(i, j) for i in range(rows) for j in range(columns)]
                self.populateGridLayout(getItemNamesFromCategory(name), positions, self.scrollItemsLayout,
                                        callback=self.mousecallbacks)

        for i in getAllItemNames():
            if name == i:
                self.placeOrder(name, self.scrollOrdersLayout, self.orders, self.total)

    def addRemoveOrderCallback(self, btnName, orderName, layout):
        self.refreshOrders(self.orders, layout, btnName, orderName, self.total)

    def placeOrder(self, name, layout, orders, lbTotal=None):

        if orders:
            for i in orders:
                if name == i[0]:
                    i[2] += 1
                    self.refreshOrders(orders, layout, self.total)

                    if lbTotal is not None:
                        total = 0
                        for y in orders:
                            total += y[1] * y[2]
                        lbTotal.setText(f"""TOTAL: {total} din""")
                        lbTotal.total = total
                    return

        howManyItems = 1
        itemPrice = int(getItemInfo(name)[2])

        tempList = [name, itemPrice, howManyItems]
        orders.append(tempList)

        order1 = QLabel(f"""{name}    {itemPrice}din    """)
        order2 = QLabel(f"""x{howManyItems}    ={itemPrice*howManyItems}din""")
        addButton = addRemoveButtons('ADD', name, layout, self.addRemoveOrderCallback)
        deleteBtn = addRemoveButtons('DELETE', name, layout, self.addRemoveOrderCallback)

        deleteBtn.setFixedSize(120, 50)
        addButton.setFixedSize(120, 50)

        order1.setAlignment(Qt.AlignLeft)
        order2.setAlignment(Qt.AlignLeft)
        layout.addRow(order1, order2)
        layout.addRow(addButton, deleteBtn)

        if lbTotal is not None:
            total = 0
            for i in orders:
                total += i[1]*i[2]
            lbTotal.setTotalText(total)
            lbTotal.total = total

    def refreshOrders(self, orders, layout, btnName=None, orderName=None, btnTotal=None):
        while True:
            item = layout.takeAt(0)
            if item:
                if item.widget():
                    item.widget().deleteLater()
            else:
                break

        if btnName == 'ADD' and orderName is not None:
            for i in orders:
                if i[0] == orderName:
                    i[2] += 1
        elif btnName == 'DELETE' and orderName is not None:
            for i in orders:
                if i[0] == orderName:
                    if i[2] <= 1:
                        orders.remove(i)
                    else:
                        i[2] -= 1

        for i in orders:
            order1 = QLabel(f"""{i[0]}    {i[1]}din    """)
            order2 = QLabel(f"""x{i[2]}    ={i[1] * i[2]}din""")
            addButton = addRemoveButtons('ADD', i[0], layout, self.addRemoveOrderCallback)
            deleteBtn = addRemoveButtons('DELETE', i[0], layout, self.addRemoveOrderCallback)

            deleteBtn.setFixedSize(120, 50)
            addButton.setFixedSize(120, 50)

            order1.setAlignment(Qt.AlignLeft)
            order2.setAlignment(Qt.AlignLeft)
            layout.addRow(order1, order2)
            layout.addRow(addButton, deleteBtn)

        if btnTotal is not None:
            total = 0
            for i in orders:
                total += i[1]*i[2]
            btnTotal.setText(f"""TOTAL: {total} din""")
            btnTotal.total = total

    def payOrder(self):
        if self.orders:

            addOrderToDailyReport(int(self.total.total))
            for i in self.orders:
                removeFromStorage(i[0], i[2])

            self.orders = []
            self.total.total = 0
            self.total.setTotalText(str(self.total.total))
            msg = msgBox('Payment', 'Order has been paid', "I")

            self.populateLayout([], self.scrollOrdersLayout, callback=self.mousecallbacks)

        else:
            msg = msgBox("Payment Failed", "There are no orders.", "W")


class categoryButton(QPushButton):
    def __init__(self, name, callback):
        super().__init__()

        self.name = name
        self.callback = callback

        if len(name) > 15:
            self.setText(splitString(self.name))
        else:
            self.setText(self.name)

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            if self.callback is not None:
                self.callback(self.name)


class itemButton(QPushButton):
    def __init__(self, name, callback):
        super().__init__()

        self.name = name
        self.callback = callback

        if len(name) > 15:
            self.setText(splitString(name))
        else:
            self.setText(self.name)

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            if self.callback is not None:
                self.callback(self.name)


class addRemoveButtons(QPushButton):
    def __init__(self, btnName, orderName, layout, callback):
        super().__init__()

        self.name = btnName
        self.orderName = orderName
        self.callback = callback
        self.parentLayout = layout

        self.setText(self.name)

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            if self.callback is not None:
                self.callback(self.name, self.orderName, self.parentLayout)


class ordersTotal(QLabel):
    def __init__(self, orderTotal):
        super().__init__()

        self.name = 'TOTAL'
        self.total = orderTotal
        self.setText(f"""{self.name} : {self.total} din""")
        self.setFixedHeight(50)
        self.setFont(QFont("Arial", 25))

    def setTotalText(self, text=None):
        if text is None:
            self.setText(f"""{self.name} : {self.total} din""")
        else:
            self.setText(f"""{self.name} : {text} din""")

    def getTotal(self):
        return int(self.total)


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


class payButton(QPushButton):
    def __init__(self, name, callback):
        super().__init__()

        self.name = name
        self.setFixedHeight(50)
        self.callback = callback

        self.setText(self.name)
        self.setStyleSheet(""" QPushButton {
            background-color: #A5F0FA;
            border-style: outset;
            border-color: black;
            border-width: 1px;
        }
        QPushButton:hover {
            background-color: #77FF6A;
        }
    """)

    def mousePressEvent(self, e):
        self.callback()
