'''
Lucas Crockett
22/09/29

View object for text adventure.

Using the passed TextEvent, shows the user a prompt and receives input.
Parses the input for keywords and returns a key for the next TextEvent.
Stops taking input after a certain number of attempts, returning the
quitKey.

__init__(qk)
    Constructor. Takes a quitKey.
Prompt(txtevt)
    Displays the prompt inside txtevt and parses input for keywords.
    Returns a key for the next TextEvent.

__quitKey
    Key to return when a force exit is triggered.
'''

from TextEventClass import TextEvent

class TextPrompt:
    #Store a quitKey so we can force quit to prevent infinite loops.
    def __init__(self, qk):
        self.__quitKey = qk

    #Show the user the prompt and receive their input. Return key for next prompt.
    def Prompt(self, txtevt):
        #Show prompt only once.
        print(txtevt.getPrompt())

        #Stop taking input after 50 invalid attempts.
        for x in range(50):
            #Take input and convert to lower case.
            userInput = input().lower()

            #Check if a keyword is present in input.
            for k in txtevt.getKeywords():
                if k.lower() in userInput:
                    #Return key for next prompt.
                    return txtevt.getNext(k)

            print("No keywords detected.")

        #User hit the max attempts, return quitKey.
        print("Looks like you aren't taking this seriously!")
        
        return self.__quitKey