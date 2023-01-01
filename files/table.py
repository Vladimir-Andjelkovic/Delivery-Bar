from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QPushButton

from files import tableOrders


class barTable(QPushButton):

    allTables = []

    def __init__(self, win):
        super().__init__(win)

        self.parentWin = win
        self.setGeometry(300, 300, 60, 60)
        self.allTables.append(self)
        self.setText("Table\n" + str(len(self.allTables)))  # write

        self.setStyleSheet(""" barTable {
            border-image: url(images/table.png);
        }""")

        self.orders = []

        self.setToolTip("Hold right mouse button to move")

        self.show()

    # Drag and drop
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            if len(self.orders) < 1:
                self.orders.append(tableOrders.orderDef(self.text(), self.parentWin))
            else:
                self.orders[0].show()

