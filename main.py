import time
import pygame
from GUI import GUI
from utility_classes import Event
from important_variables import *
from velocity_calculator import VelocityCalculator
import random
from copy import deepcopy
from card_keeper import CardKeeper
from list_keeper import ListKeeper
from card import Card

class Main:
    gui_components = GUI.get_gui_components()
    # Code below needs all of these GUI componets, so I'm unpacking the list to get them
    flip_sides_button, card_is_hard_button, show_hard_cards_only_button, term_number_text_box, shuffle_button, cards = gui_components
    is_showing_terms = True

    max_card_index = len(cards) - 1
    current_card_index = 0
    increase_event = Event()
    decrease_event = Event()
    h_button_was_clicked = False
    is_shuffled = False
    current_cards = deepcopy(cards)
    hard_cards = CardKeeper.get_hard_cards(cards)
    card = None

    def run_increase_and_decrease_logic():
        controlls = pygame.key.get_pressed()
        increase_button_clicked = controlls[pygame.K_RIGHT] or controlls[pygame.K_d]
        decrease_buttton_clicked = controlls[pygame.K_LEFT] or controlls[pygame.K_a]
        Main.increase_event.run(increase_button_clicked)
        Main.decrease_event.run(decrease_buttton_clicked)

        increase_button_is_clicked = Main.increase_event.is_click_event(
            increase_button_clicked)
        decrease_buttton_is_clicked = Main.decrease_event.is_click_event(
            decrease_buttton_clicked)


        if increase_button_is_clicked:
            Main.current_card_index = CardKeeper.get_next_index(Main.current_card_index, Main.max_card_index)

        if decrease_buttton_is_clicked:
            Main.current_card_index = CardKeeper.get_previous_index(Main.current_card_index)

        if decrease_buttton_is_clicked or increase_button_is_clicked:
            Main.card = Main.current_cards[Main.current_card_index]
            Main.card.is_showing_term = Main.is_showing_terms
            # So the card_is_hard_button resets when the next card is clicked
            Main.card_is_hard_button.set_enabled(Main.card.is_hard)

    def run_shuffle_logic():
        if not Main.shuffle_button.got_clicked():
            return

        # Code below this point will only run if the suffle button got clicked
        Main.current_card_index = 0
        Main.shuffle_button.set_enabled(not Main.shuffle_button.is_enabled)

        if Main.shuffle_button.is_enabled:
            random.shuffle(Main.current_cards)
        
        # If only showing hard cards then I'll unshuffle the hard cards
        elif Main.show_hard_cards_only_button.is_enabled:
            Main.current_cards = Main.hard_cards
        
        # If it isn't showing the hard cards, then it'll unshuffle all the cards
        else:
            Main.current_cards = deepcopy(Main.cards)
    
    def run_showing_cards_logic():
        if Main.show_hard_cards_only_button.got_clicked():
            Main.show_hard_cards_only_button.set_enabled(not Main.show_hard_cards_only_button.is_enabled)

        if Main.show_hard_cards_only_button.is_enabled and Main.show_hard_cards_only_button.got_clicked():
            Main.current_cards = CardKeeper.get_hard_cards(Main.cards)
            Main.hard_cards = deepcopy(Main.current_cards)
            Main.current_card_index = 0

        if Main.show_hard_cards_only_button.got_clicked() and not Main.show_hard_cards_only_button.is_enabled:
            Main.current_cards = deepcopy(Main.cards)

    def run_flip_sides_logic():
        if Main.flip_sides_button.got_clicked():
            Main.is_showing_terms = not Main.is_showing_terms
            Main.card.is_showing_term = Main.is_showing_terms
    
    def run_card_is_hard_logic():
        if Main.card_is_hard_button.got_clicked() and len(Main.current_cards) >= 1:
            Main.card_is_hard_button.set_enabled(not Main.card_is_hard_button.is_enabled)
            Main.card.is_hard = Main.card_is_hard_button.is_enabled
            Main.cards[Main.card.index].is_hard = Main.card_is_hard_button.is_enabled

    def run():
        while True:
            Main.max_card_index = len(Main.current_cards) - 1
            # Indexes of lists and what the user would expect to be term number are off by 1
            Main.term_number_text_box.text = f"Showing Term {Main.current_card_index + 1}/{Main.max_card_index + 1}"
            # Fill background before drawing stuff
            game_window.fill(background)
            start_time = time.time()

            if len(Main.current_cards) >= 1:
                Main.card = Main.current_cards[Main.current_card_index]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ListKeeper.save(CardKeeper.get_card_is_hard_list(Main.cards))
                    pygame.quit()

            if len(Main.current_cards) >= 1:
                Main.card.run()
            
            for component in Main.gui_components:
                # Cards are a gui component and cards are a list, so this prevents an error; lists have no attributed run
                if (type(component) != list):
                    component.run()

            functions = [Main.run_card_is_hard_logic, Main.run_flip_sides_logic, Main.run_increase_and_decrease_logic, 
                         Main.run_showing_cards_logic, Main.run_shuffle_logic]
            
            for function in functions:
                function()
            h_button_clicked = pygame.key.get_pressed()[pygame.K_h]

            if not Main.h_button_was_clicked and h_button_clicked:
                Main.card_is_hard_button.set_enabled(not Main.card_is_hard_button.is_enabled)
                Main.card.is_hard = Main.card_is_hard_button.is_enabled
                Main.cards[Main.card.index].is_hard = Main.card_is_hard_button.is_enabled

            Main.h_button_was_clicked = h_button_clicked

            pygame.display.update()
            VelocityCalculator.time = time.time() - start_time
try:
    Main.run()
except:
    pass

data = ""
divider = "}"
for card in Main.hard_cards:
    card: Card = card
    data += f"{card.term}{divider}{card.definition}\n"
file = open("bio_hard.txt", "w+")
file.write(data)
print("DONE")