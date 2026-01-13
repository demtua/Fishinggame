from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from random import uniform
from objects.fish import Fish

from objects.rod import Rod

class GameScreen(Screen):

    def on_enter(self):
        self.spawn_min = 0.5
        self.spawn_max = 2.0
        self.schedule_next_spawn()

    def schedule_next_spawn(self):
        Clock.schedule_once(self.spawn_fish, uniform(self.spawn_min, self.spawn_max))

    def spawn_fish(self, dt):
        self.add_widget(Fish(size=(50, 20)))
        self.schedule_next_spawn()

    def on_enter(self):
        # add rod ONCE
        self.add_widget(Rod())

        # fish spawning config
        self.spawn_min = 0.5
        self.spawn_max = 2.0

        # start infinite spawning
        self.schedule_next_spawn()

    def schedule_next_spawn(self):
        Clock.schedule_once(
            self.spawn_fish,
            uniform(self.spawn_min, self.spawn_max)
        )

    def spawn_fish(self, dt):
        self.add_widget(Fish())
        self.schedule_next_spawn()
