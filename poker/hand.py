###############################################################################
#
# Hand - A class to determine the strength of each player's hand.
#
# Author - Ryan Muetzel (@pretzelryan)
#

# Standard packages
from collections import Counter
from functools import partial

# Package imports.
from .card import *

# static global variables
CARDS_IN_STRAIGHT = 5
CARDS_IN_FLUSH = 5
CARDS_IN_PAIR = 2
CARDS_IN_TRIPS = 3
CARDS_IN_QUADS = 4
MAX_CARDS_IN_HAND = 5
PAIRS_IN_TWO_PAIR = 2
PAIRS_IN_ONE_PAIR = 1


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

        # Assign the first item as the start of the straight and start iteration from the second element.
        straight_start = card_type_list[0]
        for i in range(1, len(card_type_list)):

            # If the current card value is one less than the previous card, the straight continues
            if card_type_list[i].value == card_type_list[i - 1].value - 1:

                # If the straight is sufficiently long, return straight_start.
                if i - card_type_list.index(straight_start) >= CARDS_IN_STRAIGHT - 1:
                    return straight_start

            # Straight is broken, reset the starting card.
            else:
                straight_start = card_type_list[i]

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

    trips = _find_multiples(card_list, CARDS_IN_TRIPS)

    # If there is a set of trips and another pair, return the trips CardType enum.
    if trips is not CardType.HIDDEN:
        filtered_list = [card for card in card_list if card.get_type() is not trips]
        if _find_multiples(filtered_list, CARDS_IN_PAIR) is not CardType.HIDDEN:
            return trips

    return CardType.HIDDEN


def _find_two_pair(card_list: list[Card]):
    """
    Search algorithm to determine if there are two different pairs in the provided list of cards. If a two pair is
    detected, the CardType enum of the largest pair is returned.

    :param card_list: List of Card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: CardType enum of the largest pair in the two pair. If no two pair is found, returns CardType.HIDDEN.
    """

    large_pair = _find_multiples(card_list, CARDS_IN_PAIR)

    # If there is a pair and another pair, return the highest pair CardType enum.
    if large_pair is not CardType.HIDDEN:
        filtered_list = [card for card in card_list if card.get_type() is not large_pair]
        if _find_multiples(filtered_list, CARDS_IN_PAIR) is not CardType.HIDDEN:
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
    :return: List of card objects of the multiples found, up to list count. If sufficient multiples are not found,
    returns empty list.
    """

    return_card_type = _find_multiples(card_list, count)
    if return_card_type is not CardType.HIDDEN:
        return [card for card in card_list if card.get_type() is return_card_type][:count]

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
        raise ValueError("_get_pair_list() cannot get more than two pairs.")

    return_list = []

    # For pair_count get the paired cards and add them to return_list.
    for pair in range(pair_count):
        # add a pair, then filter that card out of the card_list.
        return_list.extend(_get_multiples(card_list, 2))
        card_list = [card for card in card_list if card not in return_list]

    # If the length does not match then the pairs were not found.
    if len(return_list) != pair_count * CARDS_IN_PAIR:
        raise AttributeError("get_pair_list: HandType does not match attempted best_hand assignment.")

    # fill remaining cards with the next highest cards.
    remaining_card_count = MAX_CARDS_IN_HAND - len(return_list)
    return_list.extend(_get_high_card_list(card_list, remaining_card_count))
    return return_list


def _get_set_list(card_list: list[Card], cards_in_set: int):
    """
    Gets a list of card objects, with a set of multiple cards specified put at the start of the returned list.
    After the set, the next highest cards will be placed in the list. Cards must exist in the provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :param cards_in_set: Number of multiples expected.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    return_list = []

    # Add the trips set to return_list and filter trips cards out of the card_list.
    return_list.extend(_get_multiples(card_list, cards_in_set))
    card_list = [card for card in card_list if card not in return_list]

    # If the length does not match, trips was not found.
    if len(return_list) != cards_in_set:
        raise AttributeError("get_set_list: HandType does not match attempted best_hand assignment.")

    # add the remaining high cards to return_list.
    remaining_card_count = MAX_CARDS_IN_HAND - len(return_list)
    return_list.extend(_get_high_card_list(card_list, remaining_card_count))

    return return_list


def _get_full_house_list(card_list: list[Card]):
    """
    Gets a list of card objects, with a set of three of a kind first, followed by a pair. If two sets of three of a
    kind are present, the three of a kind set with a higher value will be placed at the start of the list. Cards
    must exist in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    return_list = []

    # Add trips set to return_list and filter those cards out of card_list.
    return_list.extend(_get_multiples(card_list, CARDS_IN_TRIPS))
    card_list = [card for card in card_list if card not in return_list]

    # Add pair to return_list
    return_list.extend(_get_multiples(card_list, CARDS_IN_PAIR))

    # if the length is wrong, then this hand cannot be a full house.
    if len(return_list) != MAX_CARDS_IN_HAND:
        raise AttributeError("get_full_house_list: HandType does not match attempted best_hand assignment.")

    return return_list


def _get_flush_list(card_list: list[Card]):
    """
    Gets a list of card objects of the same suit, ordered value highest to lowest. Cards must exist in provided
    card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_HAND.
    """

    return_list = []

    # Find flush list and filter cards to only be of that suit. If the suit is hidden, there is no flush.
    flush_suit = _find_flush_suit(card_list)
    if flush_suit is Suit.HIDDEN:
        raise AttributeError("get_flush_list: HandType does not match attempted best_hand assignment.")

    card_list = [card for card in card_list if card.get_suit() is flush_suit]
    return_list.extend(_get_high_card_list(card_list, CARDS_IN_FLUSH))

    return return_list


def _get_straight_list(card_list: list[Card]):
    """
    Gets a list of card objects that are in a row, ordered highest value to lowest. Cards must exist in provided
    card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_LIST.
    """

    # If there is an ace at the start of the list, add a low ace at the end of the list (of same suit).
    if card_list[0].get_type() == CardType.ACE:
        card_list.append(Card(card_list[0].get_suit(), 1))
        card_list[-1].reveal_card()

    # Find the start value of the straight
    if len(card_list) >= CARDS_IN_STRAIGHT:
        return_list = [card_list[0]]

        for i in range(1, len(card_list)):
            # If the previous card is one bigger than the current card, add the current card to the list
            if card_list[i].get_type().value == card_list[i - 1].get_type().value - 1:
                return_list.append(card_list[i])

                if len(return_list) >= 5:
                    return return_list

            # If the previous card is not the same as current card, the straight is broken and should be reset.
            elif card_list[i].get_type().value != card_list[i - 1].get_type().value:
                return_list = [card_list[i]]

    # Straight not found, raise error.
    raise AttributeError("get_straight_list: HandType does not match attempted best_hand assignment.")


def _get_straight_flush_list(card_list: list[Card]):
    """
    Gets a list of card objects that are all suited and in a row, ordered highest value to lowest. Cards must exist
    in provided card_list.

    :param card_list: List of card objects. Should be sorted high to low and hidden cards filtered before function call.
    :return: List of card objects, up to length MAX_CARDS_IN_LIST.
    """

    # Filter for only flush cards, then call to get the straight.
    flush_suit = _find_flush_suit(card_list)
    card_list = [card for card in card_list if card.get_suit() is flush_suit]

    # If straight is not found, exception will be thrown from get_straight_list() function.
    try:
        return _get_straight_list(card_list)
    except (AttributeError, IndexError) as e:
        raise AttributeError("get_straight_flush_list: HandType does not match attempted best_hand assignment.") from e


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
        hand_dict = {HandType.QUADS:      partial(_find_multiples, self.card_list, CARDS_IN_QUADS),
                     HandType.FULL_HOUSE: partial(_find_full_house, self.card_list),
                     HandType.FLUSH:      partial(_find_flush, self.card_list),
                     HandType.STRAIGHT:   partial(_find_straight, self.card_list),
                     HandType.TRIPS:      partial(_find_multiples, self.card_list, CARDS_IN_TRIPS),
                     HandType.TWO_PAIR:   partial(_find_two_pair, self.card_list),
                     HandType.PAIR:       partial(_find_multiples, self.card_list, CARDS_IN_PAIR)}

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
                if hand_dict[hand]() is not CardType.HIDDEN:
                    self.hand_type = hand
                    break

        self._update_hand_list()

    def append_card_list(self, card_list: list[Card]):
        """
        Add a specified list of cards to the list of cards. If the list contains any element that is not a Card object,
        no elements are added.

        :param card_list: List of card objects to be added.
        :return: None.
        """

        # make sure that all of the elements are cards before adding
        if all(type(card) is Card for card in card_list):
            self.card_list += card_list

    def add_card(self, card: Card):
        """
        Add a specified card ot the list of cards. If the provided card is not a Card object, it is not added.

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

    def _update_hand_list(self):
        """
        Update best_hand to create a list of up to 5 cards that create the best hand.

        :return: None.
        """

        # Depending on the hand that was detected, call the corresponding get list function.
        hand_type_dict = {HandType.ROYAL_FLUSH:    partial(_get_straight_flush_list, self.card_list),
                          HandType.STRAIGHT_FLUSH: partial(_get_straight_flush_list, self.card_list),
                          HandType.QUADS:          partial(_get_set_list, self.card_list, CARDS_IN_QUADS),
                          HandType.FULL_HOUSE:     partial(_get_full_house_list, self.card_list),
                          HandType.FLUSH:          partial(_get_flush_list, self.card_list),
                          HandType.STRAIGHT:       partial(_get_straight_list, self.card_list),
                          HandType.TRIPS:          partial(_get_set_list, self.card_list, CARDS_IN_TRIPS),
                          HandType.TWO_PAIR:       partial(_get_pair_list, self.card_list, PAIRS_IN_TWO_PAIR),
                          HandType.PAIR:           partial(_get_pair_list, self.card_list, PAIRS_IN_ONE_PAIR),
                          HandType.HIGH_CARD:      partial(_get_high_card_list, self.card_list, MAX_CARDS_IN_HAND),
                          HandType.NOT_EVALUATED:  partial(_get_high_card_list, self.card_list, MAX_CARDS_IN_HAND)}

        self.best_hand = hand_type_dict[self.hand_type]()
