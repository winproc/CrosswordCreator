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
        Counted = []

        for Character in String:
            if Character in CharacterList:
                if not (Character in Counted):
                    CharacterList[Character] += 1
                    Counted.append(Character)
            else:
                CharacterList[Character] = 1
                Counted.append(Character)
    
    return CharacterList



def GenerateCanvas(Size):
    CanvasDict = {}

    for XIndex in range(1, Size + 1):
        for YIndex in range(1, Size + 1):
            CanvasDict['{0},{1}'.format(XIndex, YIndex)] = '-'
    
    return CanvasDict