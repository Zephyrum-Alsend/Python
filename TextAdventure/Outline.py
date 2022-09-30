'''
Text adventure game
MVC

----Model----
Dictionary of objects
class TextEvent
    def __init__(self, k, p, n):
        self.__key = k = 0123456789
        self.__prompt = p = ""
        self.__next = n = {
            "keyword" : nextKey,
        }

    def getPrompt(self):
        return self.__prompt

    def getKey(self):
        return self.__key

    def getKeywords(self):
        return self.__next.keys()

    #handle error catching in View
    def getNext(self, keyword):
        return self.__next[keyword]

Model = {
    TextEvent.getKey() : TextEvent,
}

def InitModel():
    dict = {}
    dict[k] = TextEvent(k, "prompt", {"keyword": nextKey,})
    dict[k] = TextEvent(k, "prompt", {"keyword": nextKey,})
    ...
    return dict

----View----
Pass in whole EventText object
Return key for the next EventText

def View(obj):
    print(obj.getPrompt())

    while(True):
        userInput = input().lower()

        if "quit" in userInput:
            Quit()

        for k in obj.getKeywords().lower():
            if k in userInput:
                return obj.getNext(k)

        print("No keyword detected.")

def Quit():
    exit(0)
'''