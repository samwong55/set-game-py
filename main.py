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
        self.quit = None

        self.unusedCards = []
        self.usedCards = []

        self.selected_cards = []

        self.generateAllCards()
        self.drawStatusLabel()
        self.drawQuitButton()
        self.drawCardButtons()

    def addCardToSelected(self, card_button):
        print(card_button.number, card_button.fill, card_button.shape, card_button.colour)

        if card_button in self.selected_cards:
            return

        card_button.configure(highlightbackground="#30FFFF")

        self.selected_cards.append(card_button)

        if len(self.selected_cards) == 3:
            found_set = CardButton.check_set(self.selected_cards)
            if found_set:
                msg = "Found a set :)"
            else:
                msg = "Not a set :("
            print(msg)
            self.statusLabel.configure(text=msg)
            for card in self.selected_cards:
                card.configure(highlightbackground="white")
            self.selected_cards = []
        else:
            self.statusVar.set("---")

    def drawCardButtons(self):

        for i in range(0,4):
            for j in range(0,3):
                card_index = random.randint(0, len(self.unusedCards)-1)
                new_card = self.unusedCards.pop(card_index)
                new_card.configure(
                    command=partial(self.addCardToSelected, new_card))
                new_card.grid(row=i, column=j)

    def drawQuitButton(self):

        self.quit = Button(self, text="QUIT", highlightbackground="red", command=self.destroy)
        self.quit.grid(row=5, column=1)

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


win = MainWindow()
win.mainloop()
