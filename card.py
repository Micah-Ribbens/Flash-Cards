from clickable_component import ClickableComponent
from utility_functions import percentage_to_number, draw_font
from important_variables import *
import pygame
pygame.init()


class Card(ClickableComponent):
    term = ""
    definition = ""
    is_editable = False
    font_size = 0
    text_color = None
    background_color = None
    is_showing_term = True
    font_ch_length = 0
    font_ch_height = 0
    is_hard = False

    def __init__(self, term, definition, font_size, text_color, background_color):
        self.term, self.definition = self.clean_string(
            term), self.clean_string(definition)
        self.font_size, self.text_color = font_size, text_color
        font = pygame.font.Font('freesansbold.ttf', self.font_size)
        self.background_color = background_color
        self.color = background_color
        text = font.render("a", True, background, background)
        text_rect = text.get_rect()
        # Dividing by 1.2 because not all characters are the same length
        self.font_ch_length = text_rect.width
        self.font_ch_height = text_rect.height
        super().__init__()

    def render(self):
        # Needs to be here, so doesn't draw over text
        font = pygame.font.Font('freesansbold.ttf', self.font_size)
        self.draw()

        text = self.term if self.is_showing_term else self.definition
        words_and_locations = self.get_words_and_location(text)
        current_index = 0
        current_height = self.y_coordinate
        max_index = len(text)
        max_text_length = int(screen_length / self.font_ch_length)
        # It renders line by line, so if the string is too long it won't go off screen
        while current_index < max_index:
            last_word_index = self.get_last_word_index(
                words_and_locations, current_index + max_text_length)
            text_being_rendered = self.get_all_words(
                words_and_locations, current_index, last_word_index)
            draw_font(text_being_rendered, font, x_coordinate=self.x_coordinate,
                      y_coordinate=current_height, text_color=self.text_color, background_color=self.background_color)
            current_height += self.font_ch_height + screen_height * .05
            current_index = last_word_index + 1

    def clean_string(self, string):
        """Returns a string that has characters that should be seen like letters, '', ;, etc."""
        acceptable_chs = 'abcdefghijklmnopqrstuvwxyz;,.""|/:1234567890+=- '
        cleaned_string = ""
        for ch in string:
            if acceptable_chs.__contains__(ch.lower()):
                cleaned_string += ch
        return cleaned_string

    # Gives the words locations in relation to the sentence for instance if 1, 2, and 3 were words then in the string "123"
    # It would look like {1: 0, 2:1, 3:2}
    def get_words_and_location(self, text):
        word = ""
        words_and_locations = {}
        for x in range(len(text)):
            ch = text[x]
            if ch == " ":
                words_and_locations[x] = word
                word = ""

            else:
                word += ch
        # The last word won't have a space after it
        words_and_locations[len(text)] = word

        return words_and_locations

    def get_last_word_index(self, word_and_locations: dict, index):
        word_indexes = sorted(word_and_locations.keys())
        max_word_index = 0
        for word_index in word_indexes:
            if word_index <= index and word_index > max_word_index:
                max_word_index = word_index
        return max_word_index

    def get_all_words(self, words_and_locations, start_index, end_index):
        all_indexes = words_and_locations.keys()
        all_words = ""

        for index in all_indexes:
            if index >= start_index and index <= end_index:
                all_words += words_and_locations.get(index) + " "
        return all_words

    def run(self):
        if self.got_clicked():
            self.flip()

        self.render()

    def flip(self):
        self.is_showing_term = not self.is_showing_term
