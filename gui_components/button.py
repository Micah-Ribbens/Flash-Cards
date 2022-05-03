from gui_components.clickable_component import ClickableComponent
from gui_components.text_box import TextBox


class Button(TextBox):
    enabled_color = None
    disabled_color = None
    current_color = None
    is_enabled = False

    def __init__(self, text, font_size, enabled_color, disabled_color, default_color_is_enabled, background_color):
        self.text = text
        self.enabled_color, self.disabled_color = enabled_color, disabled_color
        self.current_color = self.enabled_color if default_color_is_enabled else self.disabled_color

        super().__init__(text, font_size, False, self.current_color, background_color)

    def set_enabled(self, is_enabled):
        if is_enabled:
            self.enable()

        else:
            self.disable()

    def disable(self):
        self.set_color(self.disabled_color)
        self.is_enabled = False
    
    def enable(self):
        self.set_color(self.enabled_color)
        self.is_enabled = True
