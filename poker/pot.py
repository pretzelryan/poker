###############################################################################
#
# Pot - A class to track the money and players in each pot/side pot.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Package imports.
from .player import Player


class Pot:
    """
    A class to track the money and players in each pot/side pot.

    """

    def __init__(self):
        """
        Constructor.

        """
        self.chip_total = float(0)
        self.player_list = []
        self.betting_active = True

    def __repr__(self):
        return "Pot size: " + str(self.get_chip_total())

    def get_chip_total(self) -> float:
        """
        Accessor for the total chips in the pot.

        :return: Float for the total number of chips.
        """
        return self.chip_total

    def add_player(self, player: Player):
        """
        Adds an eligible player into the pot.

        :param player: Player object who is active in the pot.
        :return: None
        """
        self.player_list.append(player)

    # TODO: Add money to pot
    # TODO: Evaluate pot winner (Maybe do outside of this class)
