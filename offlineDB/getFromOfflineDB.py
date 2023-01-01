import xml.etree.ElementTree as ET


# Gets all categories from offDB with option to get one specific
def getItemCategory(itemCategory=""):
    res = []

    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    for i in root:
        if itemCategory == "":
            res.append(i.tag.replace("_", " "))
        elif itemCategory == i.tag.replace("_", " "):
            res.append(i.tag.replace("_", " "))
    return res


# If category is None, return all items
def getItemsFromCategory(category=None):
    res = []

    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    tempList = []

    if category is not None:
        for i in root:
            if i.tag.replace("_", " ") == category:
                for y in i:
                    tempList.append(y.tag.replace("_", " "))
                    tempList.append(y.attrib["quantity"])
                    tempList.append(y.attrib["price"])
                    tempList.append(category)

                    res.append(tempList)
                    tempList = []
    else:
        for i in root:
            for y in i:
                tempList.append(y.tag.replace("_", " "))
                tempList.append(int(y.attrib["quantity"]))
                tempList.append(int(y.attrib["price"]))
                tempList.append(i.tag)

                res.append(tempList)
                tempList = []

    return res


def getItemInfo(itemName):
    res = []
    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    for i in root:
        for y in i:
            if y.tag.replace("_", " ") == itemName:
                res.append(itemName)
                res.append(y.attrib["quantity"])
                res.append(y.attrib["price"])
                res.append(i.tag.replace("_", " "))

    return res


def getAllItemNames():
    res = []
    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    tempList = []
    for i in root:
        for y in i:
            # tempList.append(y.tag.replace("_", " "))
            # res.append(tempList)
            # tempList = []
            res.append(y.tag.replace("_", " "))
    return res


def getItemNamesFromCategory(category):
    res = []
    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    for i in root:
        if i.tag.replace("_", " ") == category:
            for y in i:
                res.append(y.tag.replace("_", " "))
    return res


def searchPartialItem(searchText):
    res = []
    tree = ET.parse("offlineDB/offlineDB.xml")
    root = tree.getroot()

    text = searchText.upper()
    tempList = []
    for i in root:
        for y in i:
            if y.tag.replace("_", " ").startswith(text):
                tempList.append(y.tag.replace("_", " "))
                tempList.append(y.attrib["quantity"])
                tempList.append(y.attrib["price"])
                tempList.append(i.tag.replace("_", " "))

                res.append(tempList)
                tempList = []

    return res


def getLoginInfo(username, pwd):
    res = []

    tree = ET.parse("offlineDB/loginDetail.xml")
    # tree = ET.parse("loginDetails.xml")
    root = tree.getroot()

    for i in root:
        for y in i:
            if y.tag == username:
                if y.attrib['pwd'] == pwd:
                    res.append(1)

    return res


def getDailyReport():

    tree = ET.parse("offlineDB/dailyReport.xml")
    root = tree.getroot()

    for i in root:
        if i.tag == "TODAY":
            return i.text
