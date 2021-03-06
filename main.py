from tkinter import *
from card import CardLabelButton, Colour, ColourCode, Fill, Shape
from PIL import ImageTk, Image
import random


class MainWindow(Tk):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.title("Python Tkinter SET Game")
        self.minsize(500, 400)

        self.fifthRowExists = False
        self.statusLabel = None
        self.statusVar = None
        self.quitBTN = None
        self.restartBTN = None

        self.unusedCards = []

        self.board_cards = []
        self.selected_cards = []

        self.generateAllCards()
        self.drawAddRowButton()
        self.drawStatusLabel()
        self.drawQuitButton()
        self.drawCardButtonsNewGame()

    def addNewRow(self):
        if not self.fifthRowExists:
            for col in range(0, 3):
                self.placeNewCard(4, col)
            self.fifthRowExists = True
        else:
            self.updateStatus("Already dealt fifth row!")

    def checkGameEnd(self):
        if len(self.unusedCards) == 0:
            return True
        return False

    def drawAddRowButton(self):
        self.addRowBTN = Button(self, text="Add New Row", command=self.addNewRow)
        self.addRowBTN.grid(row=5, column=0)

    def drawCardButtonsNewGame(self):

        for row in range(0, 4):
            for column in range(0, 3):
                self.placeNewCard(row, column)

    def drawQuitButton(self):

        self.quitBTN = Button(self, text="QUIT", background="red", command=self.destroy)
        self.quitBTN.grid(row=5, column=2)

    def drawStatusLabel(self):

        self.statusVar = StringVar()
        self.statusLabel = Label(self, text="Welcome to SET!")
        self.statusLabel.grid(row=5, column=1)

    def generateAllCards(self):
        i = 1
        for num in range(1, 4):
            for colour in Colour:
                for fill in Fill:
                    for shape in Shape:

                        bg_img = Image.open("./img/gif/white-bg.gif")
                        bg_img = bg_img.resize((round(bg_img.size[0] * 0.5), round(bg_img.size[1] * 0.5)))
                        bg_img = bg_img.convert("RGBA")

                        img = Image.open("./img/gif/1-{0}-{1}-{2}.gif".format(
                            fill.name.lower(),
                            "transparent",
                            shape.name.lower()
                        ))
                        img = img.resize((round(img.size[0] * 0.5), round(img.size[1] * 0.5)))
                        img = img.convert("RGBA")

                        width = img.size[0]
                        if num == 1:
                            bg_img.paste(img, (width, 0))
                        elif num == 2:
                            bg_img.paste(img, (round(bg_img.size[0] * 0.5) - width, 0))
                            bg_img.paste(img, (round(bg_img.size[0] * 0.5), 0))
                        else:
                            bg_img.paste(img, (0, 0))
                            bg_img.paste(img, (width, 0))
                            bg_img.paste(img, (width * 2, 0))

                        test = ImageTk.PhotoImage(bg_img)

                        temp_but = CardLabelButton(num, colour, fill, shape,
                                                   background=ColourCode[colour.name].value,
                                                   border=0,
                                                   highlightbackground="white",
                                                   highlightthickness=3,
                                                   compound="right",
                                                   image=test)
                        temp_but.image = test
                        self.unusedCards.append(temp_but)
                        i += 1

    def placeNewCard(self, row, column):
        card_index = random.randint(0, len(self.unusedCards) - 1)

        new_card = self.unusedCards.pop(card_index)
        new_card.setClickedSlot(lambda a: self.selectCard(new_card))
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

        card_button.configure(highlightbackground="blue", relief="sunken")

        self.selected_cards.append(card_button)

        if len(self.selected_cards) == 3:
            found_set = CardLabelButton.check_set(self.selected_cards)
            if found_set:
                msg = "Found a set :)"
                if not self.checkGameEnd():
                    if self.fifthRowExists:
                        self.shiftCardsUp(self.selected_cards)
                    else:
                        self.replaceValidSet(self.selected_cards)
                else:
                    self.setGameEnd()
                    return
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

        for card in self.board_cards:
            card.clearClickedSlot()
        self.restartBTN = Button(text="Restart", background="green", command=self.restartGame)
        self.restartBTN.grid(row=5, column=0)
        self.updateStatus("Game over!")

    def shiftCardsUp(self, card_list):
        fifth_row_cards = self.grid_slaves(4)
        remaining_fifth_row_cards = []  # these cards will be moved to fill empty spaces
        for card in fifth_row_cards:
            if card not in card_list:
                remaining_fifth_row_cards.append(card)

        for card in card_list:
            # get card's position in the original 3x4 grid, replace it with a remaining 5th row card
            grid_info = card.grid_info()
            if grid_info.get('row') != '4':
                row = grid_info.get('row')
                col = grid_info.get('column')
                remaining_fifth_row_cards.pop(0).grid(row=row, column=col)
            card.destroy()
            self.board_cards = [c for c in self.board_cards if c != card]
        self.fifthRowExists = False

    def updateStatus(self, msg):
        self.statusLabel.configure(text=msg)


win = MainWindow()
win.mainloop()
