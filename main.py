from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from start_window import StartScreen
from steering_wheel_window import SteeringWheelScreen
import fastf1
import globals


class WindowManager(ScreenManager):  # creating a class that deals with screen management
    pass


class F1LiveData(App):

    def __init__(self):
        super().__init__()
        self.screen_manager = WindowManager()

    def build(self):
        start_screen = StartScreen(name="start")
        self.screen_manager.add_widget(start_screen)
        steering_wheel_screen = SteeringWheelScreen(name="steering")
        self.screen_manager.add_widget(steering_wheel_screen)
        return self.screen_manager


if __name__ == '__main__':
    globals.init()
    fastf1.Cache.enable_cache('cache')
    F1LiveData().run()
