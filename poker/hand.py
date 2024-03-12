###############################################################################
#
# Hand - A class to determine the strength of each player's hand.
#
# Author - Ryan Muetzel (@pretzelryan)
#

from enum import Enum
from card import Card


class HandType(Enum):
    """
    Enumeration for representing types of hands.

    """
    NOT_EVALUATED = 0
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    TRIPS = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    QUADS = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


class Hand:
    """
    TODO: Docs

    """
    def __init__(self):
        self.hand_type = HandType(0)
        self.card_list = []

    def __repr__(self):
        return str(self.hand_type.name).replace("_", " ").capitalize()

    def evaluate_hand(self):
        pass

    def append_card_list(self, card_list: list[Card]):
        self.card_list += card_list

    def add_card(self, card: Card):
        pass

    def clear_card_list(self):
        self.card_list = []
