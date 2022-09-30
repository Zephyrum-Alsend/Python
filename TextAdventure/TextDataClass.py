'''
Lucas Crockett
22/09/28

Model/Database for text adventure.

Contains a {key:TextEvent} dictionary constructed from Prompts.txt.
Assumes Prompts.txt is in the same directory. Will throw errors if
Prompts.txt has any problems, whether that be in reading it or in
the data it holds. If errors are within the data, they are catalogued
and reported.

__init__()
    Constructor.
__initData()
    Parses Prompt.txt, converting data into TextEvent dictionary.
__verifyData()
    Ensures all TextEvents reference valid keys.
getPrompt(key)
    Returns the TextEvent with the given key and saves progress.
getStart()
    Returns the value of __startKey.
getExit()
    Returns the value of __quitKey.
verifySave()
    Returns whether Save.txt can be opened and contains a valid key.
save(key)
    Stores the passed key in Save.txt.
__str__()
    String conversion for print().

__startKey
    The first TextEvent to display on boot.
__quitKey
    The key indicating intent to exit.
__data
    Dictionary of TextEvents. {key:TextEvent}
'''

from TextEventClass import TextEvent
import json
import sys
import os

class TextData:
    #Initializes all private variables and verifies data.
    #Will throw errors if Prompts.txt has problems.
    def __init__(self):
        self.__startKey, self.__quitKey, self.__data = self.__initData()
        self.__verifyData()

    #Parses Prompts.txt into TextEvent objects to store in a dictionary.
    def __initData(self):
        d = {}

        try:
            with open(os.path.join(sys.path[0], "Prompts.txt"), "rt") as f:
                text = f.read().splitlines()
        except:
            sys.exit("Error attempting to read Prompts.txt file.")

        #Pop off the first 5 lines.
        startKey = text.pop(0)
        quitKeyword = text.pop(0)
        quitKey = text.pop(0)
        restartKeyword = text.pop(0)
        restartKey = text.pop(0)
        
        #Initialize variables for the loop.
        inString = False
        k = ''
        p = ''
        n = {}
        for line in text:
            #Toggle whether we are inside a prompt string or not.
            if line == "'''":
                inString = not inString
                continue
            
            #If inside a prompt string, treat everything as one giant string.
            if inString:
                p += line + '\n'
                continue

            #Ignore empty lines.
            if line == '':
                continue

            #Parse {keyword:key} dictionaries and create TextEvent object.
            if line[0] == '{':
                #Parse the string as a dict.
                n = json.loads(line)
                #Append quit and restart commands.
                n[quitKeyword] = quitKey
                n[restartKeyword] = restartKey

                #Dict is the last parsed variable per object,
                #ready to convert into TextEvent and append to d.
                te = TextEvent(k, p, n)
                d[te.getKey()] = te
                #Clear all temp variables.
                k = ''
                p = ''
                n = {}
                continue

            #Interpret line as a key.
            k = line

        return (startKey, quitKey, d)

    #Checks all keys referenced in __data exist.
    #Records all misreferenced keys before reporting them.
    def __verifyData(self):
        err = ''

        for txtEvnt in self.__data.values():
            for word in txtEvnt.getKeywords():
                key = txtEvnt.getNext(word)
                if key not in self.__data.keys() and key != self.__quitKey:
                    err += key + ' referenced in ' + txtEvnt.getKey() + ' does not exist.\n'

        assert err == '', err
        return

    #Given a key, return a TextEvent object.
    def getPrompt(self, key):
        txtevt = self.__data[key]
        self.save(key) #Save after attempting to use the key, confirming it's valid.
        return txtevt

    #Return the key of the first TextEvent object.
    def getStart(self, cont):
        key = self.__startKey
        if cont:
            with open(os.path.join(sys.path[0], "Save.txt"), "r") as f:
                key = f.read()
        return key

    #Return the quitKey.
    def getExit(self):
        return self.__quitKey

    #Checks if Save.txt can be opened and contains a valid key.
    def verifySave(self):
        saveVerified = True
        try:
            with open(os.path.join(sys.path[0], "Save.txt"), "r") as f:
                key = f.read()
            assert key in self.__data.keys()
        except:
            saveVerified = False

        return saveVerified

    #Stores key in Save.txt.
    def save(self, key):
        with open(os.path.join(sys.path[0], "Save.txt"), "w") as f:
            f.write(key)
        return

    #String conversion for print().
    def __str__(self):
        s = 'start ' + self.__startKey
        s += '\nquit ' + self.__quitKey
        for x in self.__data.keys():
            s += '\n' + x + ':' + str(self.__data[x])
        return s

def test():
    test = TextData()
    print(test)

if __name__ == "__main__":
    test()