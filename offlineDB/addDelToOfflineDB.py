from xml.dom import minidom
import xml.etree.ElementTree as ET


def addItemToOffDB(itemName, itemCount, itemPrice, itemType):

    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    for i in root:
        if i.tag == itemType:
            for y in i:
                if y.tag == itemName.replace(" ", "_"):
                    return -1
            ET.SubElement(i, itemName.replace(" ", "_"), quantity=str(itemCount), price=str(itemPrice))

    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="").replace("\n", "")

    with open("offlineDB/offlineDB.xml", "w") as f:
        f.write(xmlStr)

    return 0


def deleteFromOffDB(itemName, itemType):

    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    for parent in root.findall(itemType.replace(" ", "_")):
        for element in parent.findall(itemName.replace(" ", "_")):
            parent.remove(element)

    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="").replace("\n", "")

    with open("offlineDB/offlineDB.xml", "w") as f:
        f.write(xmlStr)

    return 0


def addOrderToDailyReport(order):

    tree = ET.parse("offlineDB/dailyReport.xml")
    root = tree.getroot()

    for i in root:
        if i.tag == "TODAY":
            res = int(i.text) + order
            i.text = str(res)

    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="").replace("\n", "")

    with open("offlineDB/dailyReport.xml", "w") as f:
        f.write(xmlStr)


def resetDailyReport():
    tree = ET.parse("offlineDB/dailyReport.xml")

    root = tree.getroot()

    for i in root:
        if i.tag == "TODAY":
            i.text = "0"

    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="").replace("\n", "")

    with open("offlineDB/dailyReport.xml", "w") as f:
        f.write(xmlStr)


def removeFromStorage(itemName, num):
    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    for i in root:
        for y in i:
            if y.tag.replace("_", " ") == itemName:
                currentValue = int(y.get("quantity"))
                y.set("quantity", str(currentValue-num))

    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="").replace("\n", "")

    with open("offlineDB/offlineDB.xml", "w") as f:
        f.write(xmlStr)
