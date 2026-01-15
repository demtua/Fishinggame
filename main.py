from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.gamescreen import *
from screens.menu import *
from objects.fish import Fish
from objects.sea import Sea

from kivy.properties import NumericProperty



class FishingGameApp(App):
    score = NumericProperty(0)


    def build(self):
        fish = Fish()
        menu = Menu(name='menu')
        self.sm = ScreenManager()
        self.game_screen = GameScreen(name="game_screen")
        self.game_screen.add_widget(fish)
        self.sm.add_widget(menu)
        self.sm.add_widget(self.game_screen)
        return self.sm

    def start_game(self):
        self.sm.current = 'game_screen'

    def go_to_menu(self):
        self.game_screen.reset()
        self.score = 0
        self.sm.current = 'menu'

if __name__ == "__main__":
    FishingGameApp().run()
