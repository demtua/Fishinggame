from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from random import uniform, choice
from kivy.core.window import Window
from math import atan2, degrees


class Fish(Widget):
    speed = NumericProperty(100)
    rotation = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # FORCE size immediately
        self.size_hint = (None, None)
        self.size = (64, 64)

        self.spawn_outside_with_direction()
        Clock.schedule_interval(self.update, 0)

    def spawn_outside_with_direction(self):
        w, h = Window.size
        side = choice(("left", "right", "top", "bottom"))

        if side == "left":
            self.pos = (-self.width, uniform(0, h))
            self.vx, self.vy = uniform(0.4, 1.0), uniform(-0.5, 0.5)

        elif side == "right":
            self.pos = (w, uniform(0, h))
            self.vx, self.vy = uniform(-1.0, -0.4), uniform(-0.5, 0.5)

        elif side == "top":
            self.pos = (uniform(0, w), h)
            self.vx, self.vy = uniform(-0.5, 0.5), uniform(-1.0, -0.4)

        else:
            self.pos = (uniform(0, w), -self.height)
            self.vx, self.vy = uniform(-0.5, 0.5), uniform(0.4, 1.0)

        # normalize
        length = (self.vx ** 2 + self.vy ** 2) ** 0.5
        self.vx /= length
        self.vy /= length

        # set rotation ONCE
        self.rotation = degrees(atan2(self.vy, self.vx))

    def update(self, dt):
        self.x += self.vx * self.speed * dt
        self.y += self.vy * self.speed * dt

        if self.is_outside_screen():
            Clock.unschedule(self.update)
            if self.parent:
                self.parent.remove_widget(self)

    def is_outside_screen(self):
        w, h = Window.size
        return (
            self.right < 0 or
            self.x > w or
            self.top < 0 or
            self.y > h
        )
