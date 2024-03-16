###############################################################################
#
# Testing file to verify card class is working as intended.
# Also tests the handType enumerations.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Standard imports.
import unittest


# Package imports.
from poker import hand
from poker import card


class TestHand(unittest.TestCase):
    def test_repr(self):
        new_hand = hand.Hand()
        self.assertEqual(str(new_hand), "Not evaluated", "TEST1: __repr__ did not return 'Not evaluated'.")

    def test_get_hand_type(self):
        new_hand = hand.Hand()
        self.assertEqual(new_hand.get_hand_type(), hand.HandType.NOT_EVALUATED, "TEST2: get_hand_type() did not return "
                                                                                "HandType.NOT_EVALUATED.")

    def test_add_card(self):
        new_hand = hand.Hand()
        new_card = card.Card(2, 11)
        new_card.reveal_card()
        new_hand.add_card(new_card)

        self.assertEqual(new_hand.card_list, [new_card], "TEST3: add_card did not add card to hand.card_list.")

    def test_add_multiple_cards(self):
        new_hand = hand.Hand()
        card_list = []

        new_card = card.Card(1, 10)     # Ten of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        new_card = card.Card(2, 11)     # Jack of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        new_card = card.Card(4, 3)      # Three of Diamonds
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        self.assertEqual(new_hand.card_list, card_list, "TEST4: add_card did not add successive cards to "
                                                        "hand.card_list.")

    def test_append_card_list(self):
        new_hand = hand.Hand()
        card_list1 = []
        card_list2 = []

        new_card = card.Card(1, 10)     # Ten of Spades
        new_card.reveal_card()
        card_list1.append(new_card)

        new_card = card.Card(2, 11)     # Jack of Hearts
        new_card.reveal_card()
        card_list1.append(new_card)

        new_card = card.Card(4, 3)      # Three of Diamonds
        new_card.reveal_card()
        card_list2.append(new_card)

        new_hand.append_card_list(card_list1)
        new_hand.append_card_list(card_list2)

        self.assertEqual(new_hand.card_list, card_list1 + card_list2, "TEST5: append_card_list did not add successive "
                                                                      "card lists to hand.card_list.")

    def test_filter_hidden_cards(self):
        new_hand = hand.Hand()
        card_list = []

        new_card = card.Card(1, 10)             # Ten of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        new_card = card.Card(2, 11)             # Jack of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        new_hand.add_card(card.Card(3, 13))     # Add Hidden King of Clubs

        new_card = card.Card(4, 3)              # Three of Diamonds
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        new_hand.add_card(card.Card(3, 10))     # Add Hidden Ten of Clubs

        new_hand._filter_hidden_cards()         # Call private method for sake of testing.
        self.assertEqual(new_hand.card_list, card_list, "TEST6: _filter_hidden_cards did not filter hidden cards.")

    def test_clear_card_list(self):
        new_hand = hand.Hand()
        card_list = []

        new_card = card.Card(1, 10)  # Ten of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        new_card = card.Card(2, 11)  # Jack of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)
        card_list.append(new_card)

        new_hand.clear_card_list()
        self.assertEqual(new_hand.card_list, [], "TEST7: Cards remained in hand.card_list after clear_card_list.")

    def test_high_card(self):
        new_hand = hand.Hand()

        for i in range(2, 12, 2):
            new_card = card.Card(i % 3 + 1, i)      # Generate 2, 4, 6, 8, and 10 of alternating suits.
            new_card.reveal_card()
            new_hand.add_card(new_card)

        new_hand.evaluate_hand()
        self.assertEqual(new_hand.get_hand_type(), hand.HandType.HIGH_CARD, "TEST8: Expected HandType.HIGH_CARD. "
                                                                            "Actual " + str(new_hand.get_hand_type()))

    def test_pair(self):
        new_hand = hand.Hand()

        new_card = card.Card(1, 10)  # Ten of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(1, 11)  # Jack of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(2, 10)  # Ten of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(2, 12)  # Queen of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_hand.evaluate_hand()
        self.assertEqual(new_hand.get_hand_type(), hand.HandType.PAIR, "TEST9: Expected HandType.PAIR. "
                                                                       "Actual " + str(new_hand.get_hand_type()))

    def test_two_pair(self):
        new_hand = hand.Hand()

        new_card = card.Card(1, 10)  # Ten of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(1, 12)  # Queen of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(3, 2)  # Two of Clubs
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(2, 10)  # Ten of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(2, 12)  # Queen of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_hand.evaluate_hand()
        self.assertEqual(new_hand.get_hand_type(), hand.HandType.TWO_PAIR, "TEST10: Expected HandType.TWO_PAIR. "
                                                                       "Actual " + str(new_hand.get_hand_type()))

    def test_trips(self):
        new_hand = hand.Hand()

        new_card = card.Card(1, 10)  # Ten of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(1, 12)  # Queen of Spades
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(3, 10)  # Ten of Clubs
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_card = card.Card(2, 10)  # Ten of Hearts
        new_card.reveal_card()
        new_hand.add_card(new_card)

        new_hand.evaluate_hand()
        self.assertEqual(new_hand.get_hand_type(), hand.HandType.TRIPS, "TEST11: Expected HandType.TRIPS. "
                                                                           "Actual " + str(new_hand.get_hand_type()))

    def test_straight(self):
        new_hand = hand.Hand()

        for i in range(4, 10):
            new_card = card.Card(i % 3 + 1, i)  # Generate 4, 5, 6, 7, 8, and 9 of alternating suits.
            new_card.reveal_card()
            new_hand.add_card(new_card)

        new_hand.evaluate_hand()
        self.assertEqual(new_hand.get_hand_type(), hand.HandType.STRAIGHT, "TEST12: Expected HandType.STRAIGHT. "
                                                                           "Actual " + str(new_hand.get_hand_type()))

    def test_flush(self):
        new_hand = hand.Hand()

        for i in range(2, 12, 2):
            new_card = card.Card(1, i)  # Generate 2, 4, 6, 8, and 10 of Spades.
            new_card.reveal_card()
            new_hand.add_card(new_card)

        new_hand.evaluate_hand()
        self.assertEqual(new_hand.get_hand_type(), hand.HandType.FLUSH, "TEST12: Expected HandType.FLUSH. "
                                                                           "Actual " + str(new_hand.get_hand_type()))


if __name__ == "__main__":
    unittest.main()
