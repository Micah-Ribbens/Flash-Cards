from gui_components.clickable_component import ClickableComponent
from base.utility_functions import draw_font
import pygame
pygame.init()


class TextBox(ClickableComponent):
    text = ""
    is_editable = False
    font_size = 0
    text_color = None
    background_color = None
    font = None

    def __init__(self, text, font_size, is_editable, text_color, background_color):
        self.text, self.font_size = text, font_size
        self.is_editable, self.text_color = is_editable, text_color
        self.background_color = background_color
        self.color = background_color
        self.font = pygame.font.Font('freesansbold.ttf', font_size)

        super().__init__()


    def set_font(self, font_size):
        self.font = pygame.font.Font('freesansbold.ttf', font_size)

    def render(self):
        # Needs to be hear, so doesn't draw over text
        self.draw()
        draw_font(self.text, self.font, x_coordinate=self.x_coordinate,
                  y_coordinate=self.y_coordinate, text_color=self.text_color, background_color=self.background_color)

    def run(self):
        self.render()


