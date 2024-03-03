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
    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    HIDDEN = 4
