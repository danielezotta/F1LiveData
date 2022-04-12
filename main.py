from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from start_screen import StartScreen
from quali_wheel_screen import QualiWheelScreen
from quali_steering_wheel_screen import QualiSteeringWheelScreen
import fastf1
import globals


class F1LiveData(App):

    def __init__(self):
        super().__init__()
        self.screen_manager = ScreenManager(transition=NoTransition())

    def build(self):
        start_screen = StartScreen(name="start")
        self.screen_manager.add_widget(start_screen)
        quali_wheel_screen = QualiWheelScreen(name="quali_steering")
        self.screen_manager.add_widget(quali_wheel_screen)
        quali_steering_wheel_screen = QualiSteeringWheelScreen(name="quali_steering_data")
        self.screen_manager.add_widget(quali_steering_wheel_screen)
        return self.screen_manager


if __name__ == '__main__':
    globals.init()
    fastf1.Cache.enable_cache('cache')
    F1LiveData().run()
