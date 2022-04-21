""" Copyright (c) 2022 Daniele Zotta

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE. """


from kivy.config import Config
# Needs to be here, otherwise wont work
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from quali_comparison_circuit_screen import QualiComparisonCircuitScreen
from quali_comparison_screen import QualiComparisonScreen
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
        quali_comparison_screen = QualiComparisonScreen(name="quali_comparison")
        self.screen_manager.add_widget(quali_comparison_screen)
        quali_comparison_circuit_screen = QualiComparisonCircuitScreen(name="quali_comparison_circuit")
        self.screen_manager.add_widget(quali_comparison_circuit_screen)
        return self.screen_manager


if __name__ == '__main__':
    globals.init()
    fastf1.Cache.enable_cache('cache')
    F1LiveData().run()
