###############################################################################
#
# Card - An enumeration for representing the suits of cards.
#
# Author - Ryan Muetzel (@pretzelryan)
#

from enum import Enum


class Suit(Enum):
    """
    Enumeration for representing suits of cards.

    """
    SPADES = 1
    HEARTS = 2
    CLUBS = 3
    DIAMONDS = 4
    HIDDEN = 5
