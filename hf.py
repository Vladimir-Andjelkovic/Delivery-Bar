import math


# Splits string into two with new line
def splitString(string):
    res = ""
    words = string.split(' ')
    middle = math.floor((len(words)-1)/2)
    for i in words:
        if len(i) > 11:
            res += i + "\n"
        elif words.index(i) == middle:
            res += i + "\n"
        else:
            res += i + " "
    return res
