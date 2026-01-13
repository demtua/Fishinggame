from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window


class Rod(Widget):
    end_x = NumericProperty(0)
    end_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = Window.size
        self.pos = (0, 0)

        self.end_x = Window.width / 2
        self.end_y = Window.height / 2

        Window.bind(mouse_pos=self.on_mouse_move, size=self.on_resize)

    def on_mouse_move(self, window, pos):
        self.end_x, self.end_y = pos

    def on_resize(self, *args):
        self.size = Window.size
