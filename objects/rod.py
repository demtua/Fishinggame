from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty
from kivy.core.window import Window
from kivy.clock import Clock


class Rod(Widget):
    tip_y = NumericProperty(0)

    throwing = BooleanProperty(False)
    thrown = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = Window.size
        self.pos = (0, 0)
        self.current_mouse_y = None
        self.last_mouse_y = None
        self.last_mouse_y = None
        self.throw_threshold = 1200   # pixels/sec
        self.pull_threshold = -1200

        Window.bind(mouse_pos=self.on_mouse_move, size=self.on_resize)
        Clock.schedule_interval(self.update, 0)

    def on_resize(self, *args):
        self.size = Window.size

    def on_mouse_move(self, window, pos):
        x, y = pos
        self.current_mouse_y = y

    def update(self, dt):
        if self.current_mouse_y is None:
            return

        if self.last_mouse_y is None:
            self.last_mouse_y = self.current_mouse_y
            return

        velocity = (self.current_mouse_y - self.last_mouse_y) / dt
        self.last_mouse_y = self.current_mouse_y

        # THROW (forward / up)
        if velocity > self.throw_threshold and not self.thrown:
            self.throw(velocity)

        # PULL (back / down)
        if velocity < self.pull_threshold and self.thrown:
            self.pull()

    def throw(self, velocity):
        self.throwing = True
        self.thrown = True
        self.tip_y = min(abs(velocity) * 0.15, Window.height)

    def pull(self):
        self.thrown = False
        self.throwing = False
        self.tip_y = 0
        return True

    def get_tip_pos(self):
        return self.to_parent(self.width / 2, self.tip_y)

    def reset(self):
        self.tip_y = 0
        self.throwing = False
        self.thrown = False
        self.last_mouse_y = None
