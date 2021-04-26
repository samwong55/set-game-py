from enum import Enum
from tkinter import Label

class Colour(Enum):
    GREEN = 1
    PURPLE = 2
    RED = 3


class Fill(Enum):
    EMPTY = 1
    SOLID = 2
    STRIPED = 3


class Shape(Enum):
    DIAMOND = 1
    ROUND = 2
    SQUIGGLE = 3


class CardLabelButton(Label):
    def __init__(self, number, colour, fill, shape, **kwargs):
        """
        :param  number  | <int>
        :param  colour  | <Colour>
        :param  fill    | <Fill>
        :param  shape   | <Shape>
        :param  parent  | <MainWindow>
        """
        if number not in (1, 2, 3):
            raise

        super(CardLabelButton, self).__init__(**kwargs)

        self["activebackground"] = "green"

        self.number = number
        self.colour = colour
        self.fill = fill
        self.shape = shape

    def clearClickedSlot(self):
        self.unbind("<Button-1>")

    def getText(self):
        return "{0} {1} {2} {3}{4}".format(
            self.number,
            self.fill.name.lower(),
            self.colour.name.lower(),
            self.shape.name.lower(),
            "" if self.number == 1 else "s"
        )

    def setClickedSlot(self, slot):
        self.bind("<Button-1>", slot)

    @staticmethod
    def check_colour(card1, card2, card3):
        return same_or_unique_eh(card1.colour, card2.colour, card3.colour)

    @staticmethod
    def check_fill(card1, card2, card3):
        return same_or_unique_eh(card1.fill, card2.fill, card3.fill)

    @staticmethod
    def check_number(card1, card2, card3):
        return same_or_unique_eh(card1.number, card2.number, card3.number)

    @staticmethod
    def check_shape(card1, card2, card3):
        return same_or_unique_eh(card1.shape, card2.shape, card3.shape)

    @classmethod
    def check_set(cls, card_list):
        card1 = card_list[0]
        card2 = card_list[1]
        card3 = card_list[2]
        if not cls.check_number(card1, card2, card3):
            return False
        if not cls.check_colour(card1, card2, card3):
            return False
        if not cls.check_fill(card1, card2, card3):
            return False
        if not cls.check_shape(card1, card2, card3):
            return False
        return True


def same_or_unique_eh(a, b, c):
    if a == b and b == c:
        return True
    if a != b and b != c and c != a:
        return True
    return False
