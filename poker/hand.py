###############################################################################
#
# Hand - A class to determine the strength of each player's hand.
#
# Author - Ryan Muetzel (@pretzelryan)
#

from .card import *


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
        """
        Constructor.

        """
        self.hand_type = HandType(0)
        self.card_list = []

    def __repr__(self):
        """
        String representation of the hand object.

        :return: String name of the hand.
        """
        return str(self.hand_type.name).replace("_", " ").capitalize()

    def get_hand_type(self) -> HandType:
        """
        Returns the hand type enumeration that represents the hand.

        :return: HandType enumeration.
        """
        # should evaluate_hand be called here?
        return self.hand_type

    def evaluate_hand(self):
        """
        Determines the strength of the hand to update the hand_type enumeration.

        :return: None.
        """

        # Prepare the card list by removing hidden cards and sorting high to low.
        self._filter_hidden_cards()
        self._sort_cards()

    def append_card_list(self, card_list: list[Card]):
        """
        Add a specified list of cards to the list of cards.

        :param card_list: List of card objects to be added.
        :return: None.
        """
        self.card_list += card_list

    def add_card(self, card: Card):
        """
        Add a specified card ot the list of cards.

        :param card: Card object to be added
        :return: None.
        """
        self.card_list.append(card)

    def clear_card_list(self):
        """
        Removes all cards from the card list

        :return: None.
        """
        self.card_list = []

    def _filter_hidden_cards(self):
        """
        Removes all hidden cards from the card list.

        :return: None.
        """
        self.card_list = [card for card in self.card_list if not card.is_hidden()]

    def _sort_cards(self):
        """
        Sorts the card list from highest value to lowest value.

        :return: None.
        """
        self.card_list.sort(key=lambda x: x.get_type().value, reverse=True)
