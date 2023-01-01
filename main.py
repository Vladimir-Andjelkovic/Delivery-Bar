import sys
from PyQt5.QtWidgets import QApplication
import mysql.connector as mc
from files.login import loginScreen
from offlineDB.makeOfflineDB import makeOffDB, makeOffLogins
from offlineDB.addDelToOfflineDB import resetDailyReport


app = QApplication(sys.argv)
start = loginScreen()

try:
    execute = app.exec_()

    resetDailyReport()
    try:
        dbase = mc.connect(
            host="localhost",
            port=3306,
            user="root",
            password="3221847",
            database="deliverbar"
        )
        makeOffDB()
        makeOffLogins()
    except Exception as e:
        print(e)

    sys.exit(execute)
except:
    print("Exiting...")
