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

    def __init__(self, name: str, chip_count: float):
        """
        Constructor.

        :param name: String for the player's name.
        :param chip_count: Float for the amount of money the player started with.
        """

        self.name = name
        self.chip_count = chip_count
        self.pocket = []
        self.active = True

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

    def add_card(self, card: Card):
        """
        Adds a card to the player's hand during the dealing process.

        :param card: Card to be added to the player's hand
        :return: None
        """
        if len(self.pocket) > 2:
            self.pocket.append(card)
            self.pocket[-1].reveal_card()

    def bet(self, amount):
        """
        Player puts in the first bet of the current betting round.

        :param amount: Double amount of chips bet.
        :return: Double amount bet.
        """
        self.chip_count -= amount
        return amount

    def call_raise(self, amount):
        pass

    def call(self):
        pass

    def check(self):
        pass

    def all_in(self):
        pass
