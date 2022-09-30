'''
Lucas Crockett
22/09/29

Controller for text adventure.

Handles calls to the model and view, as well as exiting.

__init__()
    Constructor.
run()
    Loops keys between the model and view until the quitKey is received.

__model
    Handles data pertaining to the text adventure.
__quitKey
    The key value signifying it's time to exit.
__view
    Handles user interaction.
'''

import TextPromptClass
import TextDataClass

class TextController:
    #Initialize TextData, TextPrompt, and store quitKey.
    def __init__(self):
        self.__model = TextDataClass.TextData()
        self.__quitKey = self.__model.getExit()
        self.__view = TextPromptClass.TextPrompt(self.__quitKey)

    #Main
    def run(self):
        key = self.__model.getStart()

        while key != self.__quitKey:
            key = self.__view.Prompt(self.__model.getPrompt(key))

        return

def test():
    test = TextController()
    test.run()

if __name__ == '__main__':
    test()