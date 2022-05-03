from clickable_component import ClickableComponent
from base.events import Event
from gui_components.text_box import TextBox
from important_variables import *
import pygame
pygame.init()


class Card(TextBox):
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
    index = 0
    space_event = None

    def __init__(self, term, definition, font_size, text_color, background_color):
        self.term, self.definition = self.clean_string(term), self.clean_string(definition)

        super().__init__(term, font_size, False, text_color, background_color)

    def clean_string(self, string):
        """Returns a string that has characters that should be seen like letters, '', ;, etc."""
        acceptable_chs = 'abcdefghijklmnopqrstuvwxyz;,.""|/:1234567890+=- '
        cleaned_string = ""
        for ch in string:
            if acceptable_chs.__contains__(ch.lower()):
                cleaned_string += ch
        return cleaned_string

    def run(self):
        self.space_event.run(pygame.key.get_pressed()[pygame.K_SPACE])
        if self.got_clicked() or self.space_event.was_clicked():
            self.flip()

        self.text = self.term if self.is_showing_term else self.definition

    def flip(self):
        self.is_showing_term = not self.is_showing_term
