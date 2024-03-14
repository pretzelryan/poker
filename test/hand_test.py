###############################################################################
#
# Testing file to verify card class is working as intended.
# Also tests the handType enumerations.
#
# Author - Ryan Muetzel (@pretzelryan)
#


from poker import hand
from poker import card


def main():
    new_hand = hand.Hand()
    print("\nHand name.  Expected: Not evaluated      Actual:", new_hand)

    new_card = card.Card(2, 11)
    new_card.reveal_card()
    new_hand.add_card(new_card)
    print("\nCard list.  Expected: [Jack of Hearts]      Actual:", new_hand.card_list)

    new_card = card.Card(3, 11)
    new_card.reveal_card()
    new_hand.append_card_list([new_card])
    print("\nCard list.  Expected: [Jack of Hearts, Jack of Clubs]      Actual:", new_hand.card_list)

    new_hand.clear_card_list()
    print("\nCard List.  Expected: []     Actual:", new_hand.card_list)

    new_card = card.Card(1, 10)
    new_card.reveal_card()
    new_hand.add_card(new_card)                 # Add Ten of Spades.
    new_card = card.Card(2, 11)
    new_card.reveal_card()
    new_hand.add_card(new_card)                 # Add Jack of Hearts.
    new_card = card.Card(4, 3)
    new_card.reveal_card()
    new_hand.add_card(new_card)                 # Add Three of Diamonds
    new_hand.add_card(card.Card(3, 10))         # Add Hidden Card (Ten of Clubs)
    print("\nCard List.  Expected: [Ten of Spades, Jack of Hearts, Three of Diamonds, Hidden Card]"
          "       Actual:", new_hand.card_list)

    new_hand.evaluate_hand()
    print("\nCard List.  Expected: [Jack of Hearts, Ten of Spades, Three of Diamonds]"
          "       Actual:", new_hand.card_list)


if __name__ == "__main__":
    main()
