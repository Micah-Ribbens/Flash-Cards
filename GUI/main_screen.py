import time
from GUI import GUI
from gui_components.text_box import TextBox
from base.utility_classes import Event
from important_variables import *
from base.velocity_calculator import VelocityCalculator
import random
from copy import deepcopy
from card_keeper import CardKeeper
from list_keeper import ListKeeper
from gui_components.button import Button
from base.colors import *

class MainScreen:
    is_showing_terms = True
    cards = CardKeeper.get_cards(text_color, text_background_color)

    # TODO events
    increase_event = Event()
    decrease_event = Event()
    shuffle_event = Event()

    current_card_index = 0
    increase_event = Event()
    decrease_event = Event()
    h_button_was_clicked = False
    is_shuffled = False
    current_cards = deepcopy(cards)
    hard_cards = CardKeeper.get_hard_cards(cards)
    card = None
    
    def __init__(self):
        text_color = white
        text_background_color = (160, 82, 45)

        self.components = cards

    def run_increase_and_decrease_logic(self):
        controlls = pygame.key.get_pressed()
        increase_button_clicked = controlls[pygame.K_RIGHT] or controlls[pygame.K_d]
        decrease_buttton_clicked = controlls[pygame.K_LEFT] or controlls[pygame.K_a]
        self.increase_event.run(increase_button_clicked)
        self.decrease_event.run(decrease_buttton_clicked)

        increase_button_is_clicked = self.increase_event.is_click_event(
            increase_button_clicked)
        decrease_buttton_is_clicked = self.decrease_event.is_click_event(
            decrease_buttton_clicked)


        if increase_button_is_clicked:
            self.current_card_index = CardKeeper.get_next_index(self.current_card_index, self.max_card_index)

        if decrease_buttton_is_clicked:
            self.current_card_index = CardKeeper.get_previous_index(self.current_card_index)

        if decrease_buttton_is_clicked or increase_button_is_clicked:
            self.card = self.current_cards[self.current_card_index]
            self.card.is_showing_term = self.is_showing_terms
            # So the card_is_hard_button resets when the next card is clicked
            self.card_is_hard_button.set_enabled(self.card.is_hard)

    def run_shuffle_logic(self):
        if not self.shuffle_button.got_clicked():
            return

        # Code below this point will only run if the suffle button got clicked
        self.current_card_index = 0
        self.shuffle_button.set_enabled(not self.shuffle_button.is_enabled)

        if self.shuffle_button.is_enabled:
            random.shuffle(self.current_cards)
        
        # If only showing hard cards then I'll unshuffle the hard cards
        elif self.show_hard_cards_only_button.is_enabled:
            self.current_cards = self.hard_cards
        
        # If it isn't showing the hard cards, then it'll unshuffle all the cards
        else:
            self.current_cards = deepcopy(self.cards)
    
    def run_showing_cards_logic(self):
        if self.show_hard_cards_only_button.got_clicked():
            self.show_hard_cards_only_button.set_enabled(not self.show_hard_cards_only_button.is_enabled)

        if self.show_hard_cards_only_button.is_enabled and self.show_hard_cards_only_button.got_clicked():
            self.current_cards = CardKeeper.get_hard_cards(self.cards)
            self.hard_cards = deepcopy(self.current_cards)
            self.current_card_index = 0

        if self.show_hard_cards_only_button.got_clicked() and not self.show_hard_cards_only_button.is_enabled:
            self.current_cards = deepcopy(self.cards)

    def run_flip_sides_logic(self):
        if self.flip_sides_button.got_clicked():
            self.is_showing_terms = not self.is_showing_terms
            self.card.is_showing_term = self.is_showing_terms
    
    def run_card_is_hard_logic(self):
        if self.card_is_hard_button.got_clicked() and len(self.current_cards) >= 1:
            self.card_is_hard_button.set_enabled(not self.card_is_hard_button.is_enabled)
            self.card.is_hard = self.card_is_hard_button.is_enabled
            self.cards[self.card.index].is_hard = self.card_is_hard_button.is_enabled

    def run(self):

        while True:
            self.max_card_index = len(self.current_cards) - 1
            # Indexes of lists and what the user would expect to be term number are off by 1
            self.term_number_text_box.text = f"Showing Term {self.current_card_index + 1}/{self.max_card_index + 1}"
            # Fill background before drawing stuff
            game_window.fill(background)
            start_time = time.time()

            if len(self.current_cards) >= 1:
                self.card = self.current_cards[self.current_card_index]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ListKeeper.save(CardKeeper.get_card_is_hard_list(self.cards))
                    pygame.quit()

            if len(self.current_cards) >= 1:
                self.card.run()

            for component in self.gui_components:
                # Cards are a gui component and cards are a list, so this prevents an error; lists have no attributed run
                if (type(component) != list):
                    component.run()

            functions = [self.run_card_is_hard_logic, self.run_flip_sides_logic, self.run_increase_and_decrease_logic,
                         self.run_showing_cards_logic, self.run_shuffle_logic]

            for function in functions:
                function()
            h_button_clicked = pygame.key.get_pressed()[pygame.K_h]

            if not self.h_button_was_clicked and h_button_clicked:
                self.card_is_hard_button.set_enabled(not self.card_is_hard_button.is_enabled)
                self.card.is_hard = self.card_is_hard_button.is_enabled
                self.cards[self.card.index].is_hard = self.card_is_hard_button.is_enabled

            self.h_button_was_clicked = h_button_clicked

            pygame.display.update()
            VelocityCalculator.time = time.time() - start_time