###############################################################################
#
# Testing file to verify player class is working as intended.
#
# Author - Ryan Muetzel (@pretzelryan)
#

from poker import player
from poker import card


def main():
    new_player = player.Player("Player 1", 1000)
    new_player.add_card(card.Card(0, 10))
    new_player.add_card(card.Card(0, 11))
    print("\nPlayer name.  Expected: Player 1       Actual:", new_player)
    print("Player's pocket.  Expected: [Ten of Spades, Jack of Spades]      Actual:", new_player.get_pocket())

    # Try to add more than two cards to player's pocket.
    new_player.add_card(card.Card(0, 14))
    print("\nPlayer's pocket.  Expected: [Ten of Spades, Jack of Spades]      Actual:", new_player.get_pocket())

    # Add second player and simulate simple betting
    second_player = player.Player("Player 2", 1500)
    second_player.add_card(card.Card(1, 11))
    second_player.add_card(card.Card(2, 11))
    pot = 0
    bet = new_player.bet(100)
    pot += bet
    pot += second_player.call(bet)
    print("\nPLayer 1 Chips.  Expected: 900     Actual:", new_player.get_chip_count())
    print("Player 2 Chips.  Expected: 1400    Actual:", second_player.get_chip_count())
    print("Pot size.  Expected: 200     Actual:", pot)

    # Player 1 all in
    bet = new_player.all_in()
    pot += bet
    pot += second_player.call(bet)
    print("\nPLayer 1 Chips.  Expected: 0     Actual:", new_player.get_chip_count())
    print("Player 2 Chips.  Expected: 500    Actual:", second_player.get_chip_count())
    print("Pot size.  Expected: 2000     Actual:", pot)


if __name__ == "__main__":
    main()
