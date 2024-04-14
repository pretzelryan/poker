###############################################################################
#
# Testing file to verify card class is working as intended.
# Also tests the cardType and suit enumerations.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Standard imports.
import unittest


# Package imports.
from poker import card


class TestHand(unittest.TestCase):
    def test_repr(self):
        new_card = card.Card(1, 2)
        self.assertEqual(str(new_card), "Hidden Card",
                         "TEST1: __repr__ did not return Hidden Card before reveal.")

    def test_get_suit(self):
        new_card = card.Card(1, 2)
        self.assertEqual(new_card.get_suit(), card.Suit.HIDDEN,
                         "TEST2: get_suit did not return HIDDEN before reveal.")

    def test_get_type(self):
        new_card = card.Card(1, 2)
        self.assertEqual(new_card.get_type(), card.CardType.HIDDEN,
                         "TEST2: get_suit did not return HIDDEN before reveal.")

    def test_repr_reveal(self):
        new_card = card.Card(1, 2)
        new_card.reveal_card()
        self.assertEqual(str(new_card), "Two of Spades",
                         "TEST4: __repr__ did not return correct card name after reveal.")

    def test_get_suit_reveal(self):
        new_card = card.Card(1, 2)
        new_card.reveal_card()
        self.assertEqual(new_card.get_suit(), card.Suit.SPADES,
                         "TEST5: get_suit did not return correct suit after reveal.")

    def test_get_type_reveal(self):
        new_card = card.Card(1, 2)
        new_card.reveal_card()
        self.assertEqual(new_card.get_type(), card.CardType.TWO,
                         "TEST6: get_suit did not return correct suit after reveal.")


if __name__ == "__main__":
    unittest.main()
