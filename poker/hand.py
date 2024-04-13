###############################################################################
#
# Hand - A class to determine the strength of each player's hand.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Standard packages
from collections import Counter

# Package imports.
from .card import *

CARDS_IN_STRAIGHT = 5
CARDS_IN_FLUSH = 5
MAX_CARDS_IN_HAND = 5


class HandType(Enum):
    """
    Enumeration for representing types of hands.

    """
    NOT_EVALUATED = 0
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    TRIPS = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    QUADS = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


def _find_multiples(card_list: list[Card], count: int):
    """
    Search algorithm to determine if there are count multiples of cards in the card list. If there are enough
    of the same card, the CardType of that set is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :param count: Number of multiples to be found.
    :return: CardType enum of the highest value multiple found.  If no multiple are found, returns CardType.HIDDEN.
    """

    # Cards should have been filtered and sorted from high to low before this function call.
    card_type_list = [card.get_type() for card in card_list]
    count_dict = Counter(card_type_list)

    # Check count of each cardType
    for card_type in count_dict:
        if count_dict[card_type] >= count:
            return card_type

    return CardType.HIDDEN


def _find_flush_suit(card_list: list[Card]):
    """
    Search algorithm to determine if there are at least 5 cards of the same suit. If there are enough suited cards,
    the Suit enumeration of that suit is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: Suit enum of the flush found. If no flush is found, returns Suit.HIDDEN.
    """

    # Cards should have been filtered and sorted from high to low before this function call.
    suit_list = [card.get_suit() for card in card_list]
    count_dict = Counter(suit_list)

    # See if a suit has 5 or more cards
    for suit in count_dict:
        if count_dict[suit] >= CARDS_IN_FLUSH:
            return suit

    return Suit.HIDDEN


def _find_flush(card_list: list[Card]):
    """
    Search algorithm to determine if there are at least 5 cards of the same suit. If there are enough suited cards,
    the CardType of the highest card of that suit is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: CardType enum of the highest card of that suit.  If no flush is found, returns CardType.HIDDEN.
    """

    flush_suit = _find_flush_suit(card_list)

    # If there is a flush get the highest value card of that suit
    if flush_suit is not Suit.HIDDEN:
        for card in card_list:
            if card.get_suit() is flush_suit:
                return card.get_type()

    return CardType.HIDDEN


def _find_straight(card_list: list[Card]):
    """
    Search algorithm to determine if there are at least 5 cards in a row. If a straight is detected, the CardType of
    the highest value card in the straight is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: CardType enum of the highest card in straight. If no straight is found, returns CardType.HIDDEN.
    """

    # Cards should have been filtered and sorted from high to low before this function call.
    # Generate a list such that there are no duplicate card types.
    card_type_list = []
    [card_type_list.append(card.get_type()) for card in card_list if card.get_type() not in card_type_list]

    # Add an ace at the end to check for a low straight.
    if card_type_list[0] == CardType.ACE:
        card_type_list.append(CardType.LOW_ACE)

    # If there are sufficient cards, iterate through the list and look for a 5 in a row.
    # Keep track of the first card in the row, and count if there are 4 more consecutive cards.
    if len(card_type_list) >= CARDS_IN_STRAIGHT:
        consecutive_cards = 1
        start_card = card_type_list[0]
        for i in range(len(card_type_list) - 1):
            consecutive_cards += 1

            # If the consecutive streak is broken then reset the starting card and the consecutive counter.
            if card_type_list[i].value != (card_type_list[i + 1].value + 1):
                consecutive_cards = 1
                start_card = card_type_list[i + 1]

            # If there are sufficient cards in a row then return the highest (first) card in the straight.
            if consecutive_cards >= CARDS_IN_STRAIGHT:
                return start_card

    # If a straight is not found.
    return CardType.HIDDEN


def _find_straight_flush(card_list: list[Card]):
    """
    Search algorithm to determine if there is a straight flush in the provided list of cards.
    A straight flush is defined as 5 cards in a row that are all the same suit. If a straight flush is detected,
    then the CardType enum of the highest card in the set is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: CardType enum of the highest card in the straight flush. If no straight flush is found,
    returns CardType.HIDDEN.
    """

    flush_suit = _find_flush_suit(card_list)

    # If there is a flush, create a new list that only contains cards of that suit and check for a straight.
    if flush_suit is not Suit.HIDDEN:
        # need to find the flush suit, rather than the highest card in the flush
        filtered_list = [card for card in card_list if card.get_suit() is flush_suit]
        return _find_straight(filtered_list)

    return CardType.HIDDEN


def _find_full_house(card_list: list[Card]):
    """
    Search algorithm to determine if there is a full house in the provided list of cards.
    A full house is defined as a set of three of a kind as well as a pair. If a full house is detected, the CardType
    enum of the trip set is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: CardType enum of the three of a kind portion of the full house. If no full house is found,
    returns CardType.HIDDEN.
    """

    trips = _find_multiples(card_list, 3)

    # If there is a set of trips and another pair, return the trips CardType enum.
    if trips is not CardType.HIDDEN:
        filtered_list = [card for card in card_list if card.get_type() is not trips]
        if _find_multiples(filtered_list, 2) is not CardType.HIDDEN:
            return trips

    return CardType.HIDDEN


def _find_two_pair(card_list: list[Card]):
    """
    Search algorithm to determine if there are two different pairs in the provided list of cards. If a two pair is
    detected, the CardType enum of the largest pair is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: CardType enum of the largest pair in the two pair. If no two pair is found, returns CardType.HIDDEN.
    """

    large_pair = _find_multiples(card_list, 2)

    # If there is a pair and another pair, return the highest pair CardType enum.
    if large_pair is not CardType.HIDDEN:
        filtered_list = [card for card in card_list if card.get_type() is not large_pair]
        if _find_multiples(filtered_list, 2) is not CardType.HIDDEN:
            return large_pair

    return CardType.HIDDEN


def _get_high_card_list(card_list: list[Card], count: int):
    """
    Gets a list of the highest cards in order from the given card list, of length up to count.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :param count: Maximum length of the returned list
    :return: List of highest card objects, up to length count.
    """

    # if count exceeds card_list length, then card list will be returned (handled by list slicing).
    return card_list[:count]


def _get_multiples(card_list: list[Card], count: int):
    """
    Gets a list of card objects with the same cardType from the provided card_list. The length of the returned list is
    equal to count, where count is the number of expected multiples. Cards must exist in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :param count: Number of multiples expected.  Ex: If trips is expected, count = 3.
    :return: List of card objects of the multiples found. If sufficient multiples are not found, returns empty list.
    """

    return_card_type = _find_multiples(card_list, count)
    if return_card_type is not CardType.HIDDEN:
        return [card for card in card_list if card.get_type() is return_card_type]

    return []


def _get_pair_list(card_list: list[Card], pair_count: int):
    """
    Gets a list of card objects, with pairs placed at the start of the list. The highest pair will be placed at the
    start of the list, and the second largest pair will be placed next. Once the pairs are placed, the remaining
    highest cards will be placed in descending order. Cards must exist in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :param pair_count: Number of pairs expected.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    # Verify that pair_count cannot exceed 2.
    # This function should be statically called, so this error should never be thrown.
    if pair_count > 2:
        raise ValueError("_get_pair_list cannot get more than two pairs.")

    # for pair_count get the pair cardType -> put those in the list first -> get remaining high cards
    # TODO
    pass


def _get_trips_list(card_list: list[Card]):
    """
    Gets a list of card objects, with a set of three of a kind at the start of the list. After the set, the next
    highest cards will be placed in the list. Cards must exist in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    # TODO
    pass


def _get_quads_list(card_list: list[Card]):
    """
    Gets a list of card objects, with a set of four of a kind at the start of the list. After the set, the next
    highest card will be placed in the list. Cards must exist in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    # TODO
    pass


def _get_full_house_list(card_list: list[Card]):
    """
    Gets a list of card objects, with a set of three of a kind first, followed by a pair. If two sets of three of a
    kind are present, the three of a kind set with a higher value will be placed at the start of the list. Cards
    must exist in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    # TODO
    pass


def _get_flush_list(card_list: list[Card]):
    """
    Gets a list of card objects of the same suit, ordered value highest to lowest. Cards must exist in provided
    card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    # TODO
    pass


def _get_straight_list(card_list: list[Card]):
    """
    Gets a list of card objects that are in a row, ordered highest value to lowest. Cards must exist in provided
    card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_LIST.
    """

    # TODO
    pass


def _get_straight_flush_list(card_list: list[Card]):
    """
    Gets a list of card objects that are all suited and in a row, ordered highest value to lowest. Cards must exist
    in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_LIST.
    """

    # TODO
    pass


class Hand:
    """
    Class to determine the strength of a player's hand.

    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################

    def __init__(self):
        """
        Constructor.

        """
        self.hand_type = HandType(0)
        self.card_list = []
        self.best_hand = []

    def __repr__(self):
        """
        String representation of the hand object.

        :return: String name of the hand.
        """
        return str(self.hand_type.name).replace("_", " ").capitalize()

    def get_hand_type(self) -> HandType:
        """
        Returns the hand type enumeration that represents the hand.

        :return: HandType enumeration.
        """
        # should evaluate_hand be called here? Maybe if the current HandType is NOT_EVALUATED?
        return self.hand_type

    def evaluate_hand(self):
        """
        Determines the strength of the hand to update the hand_type enumeration.

        :return: None.
        """

        # Prepare the card list by removing hidden cards and sorting cards by type from high to low.
        self._filter_hidden_cards()
        self._sort_cards()

        # Dictionary matches hand types with corresponding function call (excluding royal/straight flush or high card).
        # If the function call returns a value that is not equal to CardType.HIDDEN, then that hand type is present.
        hand_dict = {HandType.QUADS:        _find_multiples(self.card_list, 4),
                     HandType.FULL_HOUSE:   _find_full_house(self.card_list),
                     HandType.FLUSH:        _find_flush(self.card_list),
                     HandType.STRAIGHT:     _find_straight(self.card_list),
                     HandType.TRIPS:        _find_multiples(self.card_list, 3),
                     HandType.TWO_PAIR:     _find_two_pair(self.card_list),
                     HandType.PAIR:         _find_multiples(self.card_list, 2)}

        # Assume HandType.HIGH_CARD, which will be overwrote if a stronger hand is found.
        self.hand_type = HandType.HIGH_CARD

        # Check for royal/straight flush differently due to more complex logic.
        straight_flush_card_type = _find_straight_flush(self.card_list)
        if straight_flush_card_type is not CardType.HIDDEN:
            # A royal flush is simply an ace high straight flush.
            if straight_flush_card_type is CardType.ACE:
                self.hand_type = HandType.ROYAL_FLUSH
            else:
                self.hand_type = HandType.STRAIGHT_FLUSH

        # If there is no royal/straight flush, iterate through the dictionary to check the rest of the hand types.
        else:
            for hand in hand_dict:
                if hand_dict[hand] is not CardType.HIDDEN:
                    self.hand_type = hand
                    break

        # TODO: Should update_hand_list() be a private function?
        # self.update_hand_list()

    def update_hand_list(self):
        """
        Update best_hand to create a list of up to 5 cards that create the best hand.

        :return: None.
        """

        # pseudocode for different cases
        #
        # straight/royal flush -> filter flush and get top 5 cards from starting card
        # quads -> get all 4 quad cards, then get the next highest card
        # full house -> get the highest trips set, then get the next highest pair
        # flush -> get the highest 5 card of the given suit
        # straight -> get the highest 5 cards in a row
        # trips -> get the trip set, then the next highest 2 cards
        # two pair -> get the top 2 pairs (in order), then the highest remaining card
        # pair -> get the top pair, then the next highest 3 cards
        # high card -> get the highest 5 cards
        #
        # NOTE: the searching functions return cardType/suit enums.  Now I want to get the card object itself.

    def append_card_list(self, card_list: list[Card]):
        """
        Add a specified list of cards to the list of cards.

        :param card_list: List of card objects to be added.
        :return: None.
        """

        # make sure that all of the elements are cards before adding
        if all(type(card) is Card for card in card_list):
            self.card_list += card_list

    def add_card(self, card: Card):
        """
        Add a specified card ot the list of cards.

        :param card: Card object to be added
        :return: None.
        """
        if type(card) is Card:
            self.card_list.append(card)

    def clear_card_list(self):
        """
        Removes all cards from the card list

        :return: None.
        """
        self.card_list = []

    ###########################################################################
    #
    # Private API.
    #
    ###########################################################################

    def _filter_hidden_cards(self):
        """
        Removes all hidden cards from the card list.

        :return: None.
        """
        self.card_list = [card for card in self.card_list if not card.is_hidden()]

    def _sort_cards(self):
        """
        Sorts the card list from highest value to lowest value.

        :return: None.
        """
        self.card_list.sort(key=lambda x: x.get_type().value, reverse=True)
