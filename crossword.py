import json

def LoadStrings():
    with open("crossword_strings.csv") as Datafile:
        return Datafile.readline().split(",")

def LoadSettingFile():
    with open("settings.json") as Datafile:
        return json.loads(Datafile.read())


def GetMaxLength(Words):
    max = 0

    for i in Words:
        if len(i) > max:
            max = len(i)

    return max

def GetCharacterOccurences(WordList):
    CharacterList = {}

    for String in WordList:
        ListCopy = CharacterList

        for Char in String:
            if CharacterList[Char]:
                if ListCopy[Char] - CharacterList[Char] == 0: # Prevent duplicate chars in same string from being counted
                    ListCopy[Char] += 1
                
            else:
                ListCopy[Char] = 1

        CharacterList = ListCopy



def GenerateCanvas(Size):
    CanvasDict = {}

    for XIndex in range(1, Size + 1):
        for YIndex in range(1, Size + 1):
            CanvasDict['{0}{1}'.format(XIndex, YIndex)] = '-'
    
    return CanvasDict