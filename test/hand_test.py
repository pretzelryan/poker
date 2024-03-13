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
    print("\nHand name.  Expected: Not evaluated      Actual: ", new_hand)

    new_card = card.Card(2, 11)
    new_card.reveal_card()
    new_hand.add_card(new_card)
    print("\nCard list.  Expected: [Jack of Clubs]      Actual: ", new_hand.card_list)

    new_card = card.Card(3, 11)
    new_card.reveal_card()
    new_hand.append_card_list([new_card])
    print("\nCard list.  Expected: [Jack of Clubs, Jack of Diamonds]      Actual: ", new_hand.card_list)


if __name__ == "__main__":
    main()
