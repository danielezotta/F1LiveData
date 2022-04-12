from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from quali_wheel_screen import QualiWheelScreen
from quali_steering_wheel_screen import QualiSteeringWheelScreen
import fastf1
import globals


class F1LiveData(App):

    def __init__(self):
        super().__init__()
        self.screen_manager = ScreenManager(transition=NoTransition())

    def build(self):
        quali_wheel_screen = QualiWheelScreen(name="start")
        self.screen_manager.add_widget(quali_wheel_screen)
        quali_steering_wheel_screen = QualiSteeringWheelScreen(name="steering")
        self.screen_manager.add_widget(quali_steering_wheel_screen)
        return self.screen_manager


if __name__ == '__main__':
    globals.init()
    fastf1.Cache.enable_cache('cache')
    F1LiveData().run()
