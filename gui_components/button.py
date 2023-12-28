from gui_components.text_box import TextBox


class Button(TextBox):
    enabled_text = ""
    disabled_text = ""
    shown_text = ""
    is_enabled = False

    def __init__(self, enabled_text, disabled_text, font_size, text_color, background_color):
        self.enabled_text, self.disabled_text = enabled_text, disabled_text
        self.shown_text = disabled_text
        super().__init__(self.shown_text, font_size, False, text_color, background_color)
    
    def run(self):
        # So TextBox.render() can run it; it uses text for its name
        self.text = self.shown_text
        TextBox.render(self)
    
    def set_enabled(self, is_enabled):
        if is_enabled:
            self.enable()
        else:
            self.disable()

    def disable(self):
        self.shown_text = self.disabled_text
        self.is_enabled = False
    
    def enable(self):
        self.shown_text = self.enabled_text
        self.is_enabled = True