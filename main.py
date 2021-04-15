from tkinter import *
from card import CardButton, Colour, Fill, Shape
from functools import partial
import random


class MainWindow(Tk):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.title("Python Tkinter SET Game")
        self.minsize(500, 400)

        self.statusLabel = None
        self.statusVar = None
        self.quitBTN = None
        self.restartBTN = None

        self.unusedCards = []

        self.board_cards = []
        self.selected_cards = []

        self.generateAllCards()
        self.drawStatusLabel()
        self.drawQuitButton()
        self.drawCardButtonsNewGame()

    def checkGameEnd(self):
        if len(self.unusedCards) == 0:
            return True
        return False

    def drawCardButtonsNewGame(self):

        for row in range(0, 4):
            for column in range(0, 3):
                self.placeNewCard(row, column)

    def drawQuitButton(self):

        self.quitBTN = Button(self, text="QUIT", highlightbackground="red", command=self.destroy)
        self.quitBTN.grid(row=5, column=1)

    def drawStatusLabel(self):

        self.statusVar = StringVar()
        self.statusLabel = Label(self, text="Welcome to new game", bg="#A0A0E0", relief=RAISED)
        self.statusLabel.grid(row=5, column=0)

    def generateAllCards(self):
        i = 1
        for num in range(1, 4):
            for colour in Colour:
                for fill in Fill:
                    for shape in Shape:
                        #TODO: i think this can be changed to just use "temp_button" because we dont need a reference to each button from the main class
                        button_name = "button{0}".format(i)
                        self.__setattr__(button_name, CardButton(num, colour, fill, shape))
                        self.__getattribute__(button_name)["text"] = self.__getattribute__(button_name).getText()
                        self.unusedCards.append(self.__getattribute__(button_name))
                        i += 1

    def placeNewCard(self, row, column):
        card_index = random.randint(0, len(self.unusedCards) - 1)

        new_card = self.unusedCards.pop(card_index)
        new_card.configure(
            command=partial(self.selectCard, new_card))
        new_card.grid(row=row, column=column)
        self.board_cards.append(new_card)

    def replaceValidSet(self, card_list):

        for card in card_list:
            grid_info = card.grid_info()
            self.placeNewCard(grid_info.get('row'), grid_info.get('column'))
            card.destroy()
            self.board_cards = [c for c in self.board_cards if c != card]

    def restartGame(self):

        self.restartBTN.destroy()
        self.updateStatus("New game!")
        for card in self.board_cards:
            card.destroy()
        self.board_cards = []
        self.generateAllCards()
        self.drawCardButtonsNewGame()

    def selectCard(self, card_button):
        print(card_button.number, card_button.fill, card_button.shape, card_button.colour)

        if card_button in self.selected_cards:
            # toggle selection
            card_button.configure(highlightbackground="white")
            self.selected_cards = [c for c in self.selected_cards if c != card_button]
            return

        card_button.configure(highlightbackground="#30FFFF")

        self.selected_cards.append(card_button)

        if len(self.selected_cards) == 3:
            found_set = CardButton.check_set(self.selected_cards)
            if found_set:
                msg = "Found a set :)"
                if not self.checkGameEnd():
                    self.replaceValidSet(self.selected_cards)
                else:
                    self.setGameEnd()
            else:
                msg = "Not a set :("
                for card in self.selected_cards:
                    card.configure(highlightbackground="white")
            print(msg)
            self.updateStatus(msg)
            self.selected_cards = []
        else:
            self.statusVar.set("---")

    def setGameEnd(self):

        self.updateStatus("Game over!")
        self.restartBTN = Button(text="Restart", highlightbackground="green", command=self.restartGame)
        self.restartBTN.grid(row=5, column=2)

    def updateStatus(self, msg):
        self.statusLabel.configure(text=msg)


win = MainWindow()
win.mainloop()
