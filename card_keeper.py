from utility_functions import *
from card import Card
from list_keeper import *
class CardKeeper:
    def get_card_is_hard_list(cards):
        card_is_hard_list = []
        for card in cards:
            card_is_hard_list.append(card.is_hard)

        return card_is_hard_list

    def get_cards(text_color, text_background_color):
        cards_dictionary: dict = get_card_dictionary()
        cards = []
        for key in cards_dictionary.keys():
            term = key
            definition = cards_dictionary[key]
            card = Card(term, definition, 25, text_color, text_background_color)
            card.percentage_set_bounds(0, 10, 100, 50)
            cards.append(card)

        card_is_hard_list = ListKeeper.get()
        for x in range(len(card_is_hard_list)):
            cards[x].is_hard = card_is_hard_list[x].__contains__("True")

        return cards
    
    def get_hard_cards(cards):
        hard_cards = []
        for card in cards:
            if card.is_hard:
                hard_cards.append(card)

        return hard_cards


    def get_next_index(current_card_index, max_card_index):
        if current_card_index + 1 <= max_card_index:
            current_card_index += 1

        else:
            current_card_index = 0

        return current_card_index


    def get_previous_index(current_card_index):
        if current_card_index >= 1:
            current_card_index -= 1

        return current_card_index