###############################################################################
#
# Deck - A class to track all of the cards in the poker game.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Standard packages.
import random


# Package imports.
from .card import Card


# Global constants.
FLOP_CARD_COUNT = 3
TURN_CARD_COUNT = 1
RIVER_CARD_COUNT = 1


def generate_deck():
    """
    Generates an unshuffled 52 card standard deck.

    :return: List of 52 card objects.
    """
    deck = []
    for suit in range(4):
        deck += [Card(suit, card_type) for card_type in range(2, 15)]
    return deck


class Deck:
    """
    Class to track all of the cards in the
    """

    def __init__(self):
        """
        Constructor.

        """
        self.cards = generate_deck()
        self.burn_pile = []
        self.flop = []
        self.turn = []
        self.river = []

    def shuffle(self):
        """
        Randomly reorders the cards in the deck.

        :return: None
        """
        random.shuffle(self.cards)

    def deal_card(self) -> Card:
        """
        Removes the next card from the deck and returns it.

        :return: Card object from the deck
        """
        return self.cards.pop(0)

    def burn_card(self):
        """
        Deals the next card from the deck and places it in the burn pile.

        :return: None
        """
        self.burn_pile.append(self.deal_card())

    def deal_flop(self):
        """
        Deals the flop. Automatically burns a card before the flop is dealt.

        :return: None
        """
        self.burn_card()
        for card in range(FLOP_CARD_COUNT):
            self.flop.append(self.deal_card())
            self.flop[card].reveal_card()

    def deal_turn(self):
        """
        Deals the turn. Automatically burns a card before the flop is dealt.

        :return: None
        """
        self.burn_card()
        for card in range(TURN_CARD_COUNT):
            self.turn.append(self.deal_card())
            self.turn[card].reveal_card()

    def deal_river(self):
        """
        Deals the turn. Automatically burns a card before the flop is dealt.

        :return: None
        """
        self.burn_card()
        for card in range(TURN_CARD_COUNT):
            self.turn.append(self.deal_card())
            self.turn[card].reveal_card()
