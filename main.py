import time
import pygame
from UtilityClasses import Event
from button import Button
from clickable_component import ClickableComponent
from important_variables import *
from text_box import TextBox
from utility_functions import get_card_dictionary
from velocity_calculator import VelocityCalculator
from card import Card

readable_file = open("cards.txt", "r")
cards_dictionary: dict = get_card_dictionary()
text_color = white
text_background_color = (160, 82, 45)

def get_card_is_hard_list(cards):
    card_is_hard_list = []
    for card in cards:
        card_is_hard_list.append(card.is_hard)
    return card_is_hard_list

def list_to_string(list):
    string = "["
    max_index = len(list)
    for x in range(max_index):
        # Turns the item into a string
        item = str(list[x])

        if x != max_index - 1:
            string += item + ", "

        else:
            string += item + "]"
        
    return string

def string_to_list(string):
    skip_next_ch = False
    word = ""
    list = []
    for ch in string:
        if skip_next_ch:
            skip_next_ch = False
            continue

        if ch == "[":
            continue
        
        if ch == ",":
            skip_next_ch = True
            list.append(word)
            word = ""
            continue
        
        word += ch

        if ch == "]":
            break

    list.append(word)
    return list

def get_cards():
    # If pickle loads the cards, then this code won't load
    cards = []
    for key in cards_dictionary.keys():
        term = key
        definition = cards_dictionary[key]
        card = Card(term, definition, 25, text_color, text_background_color)
        card.percentage_set_bounds(0, 10, 100, 50)
        cards.append(card)

    try: 
        string = readable_file.read()
        card_is_hard_list = string_to_list(string)
        for x in range(len(card_is_hard_list)):
            cards[x].is_hard = card_is_hard_list[x].__contains__("True")

    except IndexError:
        print("ERROR")
        pass

    readable_file.close()
    return cards

cards = get_cards()
# So if the user is viewing the terms than they are going to be viewing definitions
# Same idea, but in reverse if definitions are showing

flip_sides_button = TextBox("Flip Sides", 20, False, text_color, green)
card_is_hard_button = Button(
    "Card Is Hard", "Card Isn't Hard", 20, text_color, green)
show_hard_cards_only_button = Button(
    "Show All Cards", "Show Only Hard Cards", 15, text_color, green)
term_number_text_box = TextBox("", 20, False, text_color, green)

card_is_hard_button.percentage_set_bounds(50, 0, 30, 10)
flip_sides_button.percentage_set_bounds(40, 90, 25, 10)
show_hard_cards_only_button.percentage_set_bounds(67, 90, 33, 10)
term_number_text_box.percentage_set_bounds(10, 0, 35, 10)
card_is_hard_button.set_enabled(cards[0].is_hard)
# Starts off showing term side and if flip_sides_button is clicked then it shows the definitions
is_showing_terms = True

max_card_index = len(cards) - 1
current_card_index = 0


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

increase_event = Event()
decrease_event = Event()
current_cards = cards

while True:
    max_card_index = len(current_cards) - 1
    # Indexes of lists and what the user would expect to be term number are off by 1
    term_number_text_box.text = f"Showing Term {current_card_index + 1}/{max_card_index + 1}"
    controlls = pygame.key.get_pressed()
    # Fill background before drawing stuff
    game_window.fill(background)
    start_time = time.time()
    increase_button_clicked = controlls[pygame.K_RIGHT] or controlls[pygame.K_d]
    decrease_buttton_clicked = controlls[pygame.K_LEFT] or controlls[pygame.K_a]
    increase_event.run(increase_button_clicked)
    decrease_event.run(decrease_buttton_clicked)

    if len(current_cards) >= 1:
        card = current_cards[current_card_index]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            card_is_hard_list = get_card_is_hard_list(cards)
            writable_file = open("cards.txt", "w")
            writable_file.write(list_to_string(card_is_hard_list))
            pygame.quit()

    if flip_sides_button.got_clicked():
        is_showing_terms = not is_showing_terms

    # So the arrow keys controll what card the person is on
    # Also need to set current_card_index to what the functions get_next_index() and get_previous_index() return so the current_card_index changes
    increase_button_is_clicked = increase_event.is_click_event(
        increase_button_clicked)
    decrease_buttton_is_clicked = decrease_event.is_click_event(
        decrease_buttton_clicked)
    if increase_button_is_clicked:
        current_card_index = get_next_index(current_card_index, max_card_index)

    if decrease_buttton_is_clicked:
        current_card_index = get_previous_index(current_card_index)

    if decrease_buttton_is_clicked or increase_button_is_clicked:
        card = cards[current_card_index]
        card.is_showing_term = is_showing_terms
        # So the card is hard button resets when the next card is clicked
        card_is_hard_button.set_enabled(card.is_hard)

    if flip_sides_button.got_clicked():
        card.is_showing_term = is_showing_terms

    if card_is_hard_button.got_clicked() and len(current_cards) >= 1:
        card_is_hard_button.set_enabled(not card_is_hard_button.is_enabled)
        card.is_hard = card_is_hard_button.is_enabled

    if show_hard_cards_only_button.got_clicked():
        show_hard_cards_only_button.set_enabled(
            not show_hard_cards_only_button.is_enabled)

    if show_hard_cards_only_button.is_enabled and show_hard_cards_only_button.got_clicked():
        current_cards = get_hard_cards(cards)
        current_card_index = 0

    elif show_hard_cards_only_button.got_clicked():
        current_cards = cards

    if len(current_cards) >= 1:
        card.run()
    flip_sides_button.run()
    show_hard_cards_only_button.run()
    card_is_hard_button.run()
    term_number_text_box.run()
    pygame.display.update()
    VelocityCalculator.time = time.time() - start_time
