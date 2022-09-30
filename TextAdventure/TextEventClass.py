'''
Lucas Crockett
22/09/28

Object containing text adventure prompts.

__init__(k, p, n)
    Constructor. Takes a key, prompt string, and {keyword:key} dictionary.
getPrompt()
    Returns __prompt.
getKey()
    Returns __key.
getKeywords()
    Returns all keys in __next.
getNext(keyword)
    Uses keyword as a key in __next to return a value.
__str__
    String conversion for print().

__key
    Identifier for this object.
__prompt
    String.
__next
    Dictionary of other TextEvent keys to go to. {keyword:key}
'''

class TextEvent:
    #Constructor
    def __init__(self, k, p, n):
        #Assert each variable is the right type, where possible.
        assert type(p) == str, "Prompt p must be a string."
        assert type(n) == dict, "Next n must be a dict."
        for x in n.keys():
            assert type(x) == str, "Keys in n must be strings."
            #Convert all keys to strings.
            n[x] = str(n[x])
        
        self.__key = str(k)
        self.__prompt = p
        self.__next = n

    #Getter for __prompt
    def getPrompt(self):
        return self.__prompt

    #Getter for __key
    def getKey(self):
        return self.__key

    #Getter for keyword keys in __next
    def getKeywords(self):
        return self.__next.keys()

    #Getter for key values in __next
    #Error handling must be performed by the caller.
    def getNext(self, keyword):
        return self.__next[keyword]

    def __str__(self):
        d = {self.__key:self.__prompt}
        for k in self.getKeywords():
            d.update({k:self.getNext(k)})

        return str(d)