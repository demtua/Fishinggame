from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.gamescreen import *
from objects.fish import Fish
from objects.sea import Sea




class FishingGameApp(App):
    def build(self):
        fish = Fish()
        sm = ScreenManager()
        self.game_screen = GameScreen(name="game_screen")
        self.game_screen.add_widget(fish)
        
        sm.add_widget(self.game_screen)
        return sm


if __name__ == "__main__":
    FishingGameApp().run()
