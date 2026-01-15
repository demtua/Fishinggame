from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from random import uniform
from kivy.app import App
from kivy.core.window import Window

from objects.fish import Fish
from objects.rod import Rod
from objects.ripple import Ripple


class GameScreen(Screen):

    def on_enter(self):
        self.ripple_active = False
        self.ripple = None
        self.rod = Rod()
        self.add_widget(self.rod)
        self.throw_consumed = False
        self.hooked_fish = None

        self.spawn_min = 0.5
        self.spawn_max = 2.0
        self.schedule_next_spawn()
        Clock.schedule_interval(self.update_ripple_position, 0)

        Clock.schedule_interval(self.check_collisions, 0)
        Clock.schedule_interval(self.check_pull, 0)

    # ---------------- SPAWNING ----------------
    def on_leave(self):
        Clock.unschedule(self.update_ripple_position)

    def schedule_next_spawn(self):
        Clock.schedule_once(
            self.spawn_fish,
            uniform(self.spawn_min, self.spawn_max)
        )

    def spawn_fish(self, dt):
        self.add_widget(Fish())
        self.schedule_next_spawn()

    # ---------------- COLLISION ----------------

    def check_collisions(self, dt):
        if not self.rod.thrown or self.throw_consumed or self.hooked_fish:
            return

        tip_x, tip_y = self.rod.get_tip_pos()

        for widget in self.children:
            if (
                isinstance(widget, Fish)
                and not widget.hooked
                and not widget.escaped   # <-- IMPORTANT
            ):
                if widget.collide_point(tip_x, tip_y):
                    widget.hooked = True
                    self.hooked_fish = widget
                    self.throw_consumed = True
                    self.start_ripple(tip_x, tip_y)
                    return
    
    
    def clear_escape_flags(self):
        for widget in self.children:
            if isinstance(widget, Fish):
                widget.escaped = False
    # ---------------- INPUT ----------------

    def on_mouse_down(self, window, x, y, button, modifiers):
        if button == 'right' and self.hooked_fish:
            self.catch_fish()

    def catch_fish(self):
        from kivy.app import App
        App.get_running_app().score += 1

        self.remove_widget(self.hooked_fish)
        self.hooked_fish = None

        self.end_ripple()

    # ---------------- RESET ----------------
    def on_ripple_timeout(self):
        if self.hooked_fish:
            self.hooked_fish.hooked = False
            self.hooked_fish = None

        self.end_ripple()

    def end_ripple(self):
        self.ripple_active = False

        if self.ripple:
            self.remove_widget(self.ripple)
            self.ripple = None

    def reset(self):
        # stop timers
        Clock.unschedule(self.check_collisions)
        Clock.unschedule(self.spawn_fish)

        # remove fish
        for widget in self.children[:]:
            if isinstance(widget, Fish):
                self.remove_widget(widget)

        # reset rod
        if self.rod:
            self.rod.reset()

        # reset state
        self.hooked_fish = None
        App.get_running_app().score = 0


    def check_pull(self, dt):
        if self.hooked_fish and self.ripple_active and not self.rod.thrown:
            self.catch_fish()
        elif self.throw_consumed and not self.rod.thrown:
            self.throw_consumed = False   # <-- RESET FOR NEXT THROW

    def update_ripple_position(self, dt):
        if self.ripple_active and self.ripple:
            tip_x, tip_y = self.rod.get_tip_pos()
            self.ripple.center = (tip_x, tip_y + self.ripple.height / 2)



    def start_ripple(self):
        self.ripple_active = True

        self.ripple = Ripple(duration=1.2)
        self.add_widget(self.ripple)

    def start_ripple(self, x, y):
        self.ripple_active = True

        self.ripple = Ripple(duration=1.2)
        self.ripple.center = (x, y)
        self.add_widget(self.ripple)

    def on_ripple_complete(self):
        self.ripple_ready = True
        if self.ripple:
            self.remove_widget(self.ripple)
            self.ripple = None