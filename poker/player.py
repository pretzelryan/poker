###############################################################################
#
# Player - A class to represent users in the game and allow them to interact with the game.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Package imports
from .card import *


class Player:
    """
    A class to represent users in the game, and allow them to interact with the game.
    Betting methods are designed to return a float if the user is remaining active, or None if the player folds.

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

    def add_card(self, card: Card):
        """
        Adds a card to the player's hand during the dealing process.

        :param card: Card to be added to the player's hand
        :return: None
        """
        if len(self.pocket) < 2:
            self.pocket.append(card)
            self.pocket[-1].reveal_card()

    def fold(self):
        """
        Player forfeits their hand. Once a player folds, they can no longer win the pot in that hand.

        :return: None
        """
        self.active = False
        return None

    def bet(self, amount: float):
        """
        Player puts in the first bet of the current betting round. Cannot bet if a bet has already been placed.
        If the total bet exceeds the player's current balance, the player will automatically all-in.

        :param amount: Float amount of chips the player is betting.
        :return: Float amount bet.
        """
        if amount < self.chip_count:
            self.chip_count -= amount
            return amount
        else:
            return self.all_in()

    def call_raise(self, current_bet: float, amount: float):
        """
        Player matches the current bet placed, and then raises the bet for the current betting round.
        If the total bet exceeds the player's current balance, the player will automatically all-in.
        This function should only be called if a bet has already been placed.

        :param current_bet: Float amount of chips that other players have bet.
        :param amount: Float total amount of chips this player is putting in the pot this betting round.
        :return:
        """
        call_amount = self.call(current_bet)
        if call_amount < current_bet:
            return call_amount
        return self.bet(amount) + call_amount

    def call(self, current_bet: float):
        """
        Player matches the current bet placed for the current betting round.
        Cannot check if a bet has not been placed.  If the current bet exceeds the player's current balance,
        the player will automatically all in.

        :param current_bet: Float amount of chips that other players have bet.
        :return: Float amount of chips this player is matching with.
        """
        if current_bet < self.chip_count:
            self.chip_count -= current_bet
            return current_bet
        else:
            return self.all_in()

    def check(self, current_bet: float):
        """
        Player does nothing during their turn. Cannot check if a bet has been placed.  If a player attempts to
        check while a bet has been placed, they will automatically fold.

        :return: Integer zero if no bet has been placed, otherwise returns False.
        """
        if current_bet > 0:
            return self.fold()
        return float(0)

    def all_in(self):
        """
        Player puts all of their remaining chips in as a bet.

        :return: Float amount bet.
        """
        chips_bet = self.chip_count
        self.chip_count = 0
        return chips_bet
