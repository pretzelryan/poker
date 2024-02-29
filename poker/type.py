###############################################################################
#
# Card - An enumeration for representing the suits of cards.
#
# Author - Ryan Muetzel (@pretzelryan)
#

from enum import Enum


class Type(Enum):
    """
    Enumeration for representing types of cards.

    """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    HIDDEN = 16

    def __repr__(self):
        """
        Returns a Capitalized string representation of the card type (ex: Jack).

        :return: String representation of card type.
        """
        return repr(self).lower()
