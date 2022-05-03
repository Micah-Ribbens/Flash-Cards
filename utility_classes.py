import pygame
from important_variables import game_window
from velocity_calculator import VelocityCalculator
from important_variables import screen_height, background, screen_length, game_window
from utility_functions import deepcopy, percentage_to_number


class Segment:
    is_percentage = False
    color = (0, 0, 0)
    amount_from_top = 0
    amount_from_left = 0
    length_amount = 0
    width_amount = 0

    def __init__(self, **kwargs):
        """is_percentage, color, amount_from_top, amount_from_left, length_amount, width_amount"""
        self.is_percentage, self.color = kwargs.get(
            "is_percentage"), kwargs.get("color"),
        self.amount_from_top, self.amount_from_left = kwargs.get(
            "amount_from_top"), kwargs.get("amount_from_left")
        self.length_amount, self.width_amount = kwargs.get(
            "length_amount"), kwargs.get("width_amount")


class GameObject:
    
    x_coordinate = 0
    y_coordinate = 0
    height = 0
    length = 0
    color = (0, 0, 250)
    name = ""
    attributes = []

    # @property automatically changes this "attribute" when the x_coordinate or length changes
    # Can be treated as an attribute
    @property
    def right_edge(self):
        return self.x_coordinate + self.length

    @property
    def bottom(self):
        return self.y_coordinate + self.height

    @property
    def x_midpoint(self):
        return self.x_coordinate + self.length / 2

    @property
    def y_midpoint(self):
        return self.y_coordinate + self.height / 2

    def __init__(self, x_coordinate=0, y_coordinate=0, height=0, length=0, color=(0, 0, 0)):
        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate
        self.height, self.length, self.color = height, length, color

    def draw(self):
        pygame.draw.rect(game_window, (self.color), (self.x_coordinate,
                                                     self.y_coordinate, self.length, self.height))


class HistoryKeeper:
    memento_list = {}

    def reset():
        HistoryKeeper.memento_list = {}

    def add(object, name, is_game_object):
        if is_game_object:
            object = deepcopy(object)

        HistoryKeeper._add(object, name)

    def _add(object, name):
        try:
            HistoryKeeper.memento_list[name].append(object)
        except KeyError:
            HistoryKeeper.memento_list[name] = [object]

    def get(name):
        if HistoryKeeper.memento_list.get(name) is None:
            return []
        return HistoryKeeper.memento_list.get(name)

    def get_last(name):
        mementos = HistoryKeeper.get(name)
        if len(mementos) == 0:
            return None
        if len(mementos) == 1:
            return mementos[0]
        return mementos[len(mementos) - 2]


class Event:
    def is_continuous(self, event):
        return HistoryKeeper.get_last(id(self)) and event

    def run(self, event):
        HistoryKeeper.add(event, id(self), False)
    
    def is_click_event(self, event):
        return event and not self.is_continuous(event)

    def happened_last_cycle(self):
        return HistoryKeeper.get_last(id(self))
