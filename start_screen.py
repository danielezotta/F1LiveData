from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import globals


class StartScreen(Screen):
    kv = Builder.load_file('start_screen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def quali_steering_clicked(self):
        self.manager.current = "quali_steering"