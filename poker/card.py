###############################################################################
#
# Card - A class for representing cards in the poker simulation.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Import suit and type enumerations.
from .suit import *
from .type import *


class Card:
    """
    Class for representing cards in the poker simulation.

    """

    def __init__(self, suit, card_type):
        """
        Constructor. See

        :param suit: Integer to specify card suit.
        :param card_type: Integer to specify card type.
        """
        self.hidden = True
        self.suit = Suit(suit)
        self.type = CardType(card_type)

    def reveal_card(self):
        """
        Allows other classes to see the value of the card (if not already visible)

        :return: None
        """
        self.hidden = False

    def __repr__(self):
        """
        Gets the string representation of the card.  If the card is hidden, returns 'Hidden Card',
        otherwise returns the card value and suit (ex: 'Jack of Hearts').

        :return: String representation of the card.
        """
        if self.hidden:
            return "Hidden Card"
        return str(self.type.name).capitalize() + " of " + str(self.suit.name).capitalize()

    def get_suit(self):
        """
        Gets the enumeration representation of the card's suit.  If the card is hidden, returns HIDDEN enum,
        otherwise returns the card suit (ex: Suit.HEART).

        :return: Enumeration representation of the card's suit.
        """
        if self.hidden:
            return Suit.HIDDEN
        return self.suit

    def get_type(self):
        """
        Gets the enumeration representation of the card's type.  If the card is hidden, returns the HIDDEN enum,
        otherwise returns the card type (ex: Type.KING).

        :return:
        """
        if self.hidden:
            return CardType.HIDDEN
        return self.type

