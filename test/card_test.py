###############################################################################
#
# Testing file to verify card class is working as intended.
# Also tests the cardType and suit enumerations.
#
# Author - Ryan Muetzel (@pretzelryan)
#

from poker import card


def main():
    new_card = card.Card(1, 2)
    print("\nDisplay card. Expected: Hidden Card      Actual:", new_card)
    print("Get card type. Expected: CardType.HIDDEN     Actual:", new_card.get_type())
    print("Get card suit. Expected: Suit.HIDDEN     Actual:", new_card.get_suit())

    new_card.reveal_card()
    print("\nDisplay card. Expected: Two of Hearts    Actual:", new_card)
    print("Get card type. Expected: CardType.TWO     Actual:", new_card.get_type())
    print("Get card suit. Expected: Suit.HEARTS     Actual:", new_card.get_suit())

    new_type = card.CardType(16)
    print("\nCard Type. Expected: Type.HIDDEN     Actual:", new_type)


if __name__ == "__main__":
    main()
