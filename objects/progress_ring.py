from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.metrics import dp

# ---------- Primitives ----------
class ProgressRing(Widget):
    value = NumericProperty(0)   # 0..100
    thickness = NumericProperty(dp(3))
    bg_color = ListProperty([0.28, 0.28, 0.32, 1])
    fg_color = ListProperty([0.62, 0.45, 1.0, 1])
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self._bgc = Color(rgba=self.bg_color)
            self._bg = Line(circle=(0,0,0, 0, 360), width=self.thickness, cap='round')
            self._fgc = Color(rgba=self.fg_color)
            self._fg = Line(circle=(0,0,0, -90, -90), width=self.thickness, cap='round')
        self.bind(pos=self._update, size=self._update, value=self._update,
                  thickness=self._update, bg_color=self._recolor, fg_color=self._recolor)

    def _recolor(self, *args):
        self._bgc.rgba = self.bg_color
        self._fgc.rgba = self.fg_color

    def _update(self, *args):
        r = min(self.width, self.height) / 2 - self.thickness / 2
        cx, cy = self.center
        self._bg.circle = (cx, cy, r, 0, 360)
        end = -90 + 360 * (max(0, min(100, self.value)) / 100.0)
        self._fg.circle = (cx, cy, r, -90, end)
        self._bg.width = self.thickness
        self._fg.width = self.thickness