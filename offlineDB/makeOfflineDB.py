import xml.etree.ElementTree as ET
import mysql.connector as mc
from xml.dom import minidom


def makeOffDB():
    rawDB = []

    try:
        dbase = mc.connect(
            host="localhost",
            port=3306,
            user="root",
            password="3221847",
            database="enigmabar"
        )

        cursor = dbase.cursor()
        query = f"""SELECT item_name, item_count, item_price, item_type FROM items"""
        cursor.execute(query)
        res = cursor.fetchall()

        tempList = []
        for i in res:
            for y in i:
                tempList.append(y)
            if tempList:
                rawDB.append(tempList)
                tempList = []

    except Exception as e:
        print(e)

    underscoreMyList = []

    tempList = []

    for i in rawDB:

        for y in i:
            if type(y) == str:
                tempList.append(y.replace(" ", "_"))
            elif type(y) == int:
                tempList.append(y)

        underscoreMyList.append(tempList)
        tempList = []

    root = ET.Element("root")

    itemTypeList = []

    for i in underscoreMyList:
        if i[3] not in itemTypeList:
            itemTypeList.append(i[3])

    for i in itemTypeList:
        ET.SubElement(root, i)

    for i in root:
        for y in underscoreMyList:
            if y[3] == i.tag:
                ET.SubElement(i, y[0], quantity=str(y[1]), price=str(y[2]))

    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open("offlineDB/offlineDB.xml", "w") as f:
        f.write(xmlStr)


def makeOffLogins():

    loginData = []

    try:
        dbase = mc.connect(
            host="localhost",
            port=3306,
            user="root",
            password="3221847",
            database="enigmabar"
        )

        cursor = dbase.cursor()
        query = f"""SELECT username, pwd FROM logins"""
        cursor.execute(query)
        res = cursor.fetchall()

        tempList = []
        for i in res:
            for y in i:
                tempList.append(y)
            if tempList:
                loginData.append(tempList)
                tempList = []

    except Exception as e:
        print(e)

    root = ET.Element("root")

    loginDetails = ET.SubElement(root, "loginDetails")

    for i in loginData:
        ET.SubElement(loginDetails, i[0], pwd=i[1])

    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open("offlineDB/loginDetail.xml", "w") as f:
        f.write(xmlStr)

