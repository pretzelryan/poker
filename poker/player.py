###############################################################################
#
# Player - A class to represent users in the game and allow them to interact with the game.
#
# Author - Ryan Muetzel (@pretzelryan)
#

from .card import *


class Player:
    """
    A class to represent users in the game, and allow them to interact with the game.

    """

    def __init__(self, name: str, card1: Card, card2: Card, chip_count: float):
        """
        Constructor.

        :param name: String for the player's name.
        :param card1: Card object for the player's first pocket card.
        :param card2: Card object for the player's second pocket card.
        :param chip_count: Float for the amount of money the player started with.
        """

        self.name = name
        self.card1 = card1
        self.card2 = card2
        self.chip_count = chip_count
        self.active = True

        # Make sure the player can see their own cards.
        self.card1.reveal_card()
        self.card2.reveal_card()

    def __repr__(self):
        return self.name

    def is_player_active(self):
        """
        Returns true if the player is still active in the current hand. Otherwise false.
        Players become inactive when they fold.

        :return: Boolean true if player is active, false otherwise.
        """
        return self.active

    def fold(self):
        """
        Player forfeits their hand. Once a player folds, they can no longer win the pot in that hand.

        :return: None
        """
        self.active = False

    def bet(self):
        pass

    def call_raise(self):
        pass

    def call(self):
        pass

    def all_in(self):
        pass
