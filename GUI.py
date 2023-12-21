from text_box import TextBox
from button import Button
from important_variables import *
from card_keeper import CardKeeper
class GUI:

    def get_gui_components():
        text_color = white
        text_background_color = (160, 82, 45)
        cards = CardKeeper.get_cards(text_color, text_background_color)
        flip_sides_button = TextBox("Flip Sides", 20, False, text_color, green)
        card_is_hard_button = Button(
            "Card Is Hard", "Card Isn't Hard", 20, text_color, green)
        show_hard_cards_only_button = Button(
            "Show All Cards", "Show Only Hard Cards", 15, text_color, green)
        term_number_text_box = TextBox("", 20, False, text_color, green)
        shuffle_button = Button("Unshuffle", "Shuffle", 20, text_color, green)

        card_is_hard_button.percentage_set_bounds(50, 0, 30, 10)
        flip_sides_button.percentage_set_bounds(40, 90, 25, 10)
        show_hard_cards_only_button.percentage_set_bounds(67, 90, 33, 10)
        term_number_text_box.percentage_set_bounds(10, 0, 35, 10)
        shuffle_button.percentage_set_bounds(0, 90, 35, 10)
        card_is_hard_button.set_enabled(cards[0].is_hard)

        return [flip_sides_button, card_is_hard_button, show_hard_cards_only_button, term_number_text_box, shuffle_button, cards]
