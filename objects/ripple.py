from kivy.uix.widget import Widget
from kivy.clock import Clock
from objects.progress_ring import ProgressRing


class Ripple(Widget):
    def __init__(self, duration=1.2, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (64, 64)

        self.duration = duration
        self.elapsed = 0

        self.ring = ProgressRing(
            size_hint=(None, None),
            size=self.size,
            value=100
        )
        self.add_widget(self.ring)

        # ensure initial placement
        self.ring.center = self.center

        Clock.schedule_interval(self.update, 0)

    def on_size(self, *args):
        if hasattr(self, "ring"):
            self.ring.center = self.center

    def on_pos(self, *args):
        if hasattr(self, "ring"):
            self.ring.center = self.center

    def update(self, dt):
        self.elapsed += dt
        remaining = max(0, 1 - self.elapsed / self.duration)
        self.ring.value = remaining * 100

        if remaining <= 0:
            Clock.unschedule(self.update)
            if self.parent:
                self.parent.on_ripple_timeout()
