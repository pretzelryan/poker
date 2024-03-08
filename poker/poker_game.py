###############################################################################
#
# PokerGame - A class to run the poker game.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Package imports.
from .card import Card
from .player import Player
from .pot import Pot
from .deck import Deck


class PokerGame:
    """
    TODO: Docs

    """

    def __init__(self):
        self.player_list = []
        self.pot_list = [Pot()]
        self.deck = Deck()

    def add_player(self, player: Player):
        """
        Adds specified player to the game.

        :param player: Player object to join the game
        :return: None
        """
        self.player_list.append(player)

    def remove_player(self, player: Player):
        """
        Removes specified player from the game.

        :param player: Player object to be removed.
        :return: None
        """
        if player in self.player_list:
            self.player_list.remove(player)

    def deal_players(self):
        pass

    def evaluate_hands(self):
        pass
