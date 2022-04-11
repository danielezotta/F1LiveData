from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
import fastf1
import globals
import time
import threading
from threading import Thread


Builder.load_file('steering_wheel_window.kv')


class SteeringWheelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lap = None
        self.lap_speed = None
        self.lap_time = None
        self.speed_frequency = None
        self.simulation_going = False
        self.speed_index = None

    def on_enter(self, *args):
        self.ids.info_label.text = '%s - %s' % (globals.driver_name, globals.circuit_name)
        self.get_lap()

    def get_lap(self):
        session = fastf1.get_session(2022, globals.circuit_number, 'Q')
        session.load(laps=True, telemetry=True, weather=True)
        self.lap = session.laps.pick_driver(globals.driver_number).pick_fastest()
        self.lap_speed = self.lap.telemetry['Speed']
        self.lap_time = self.lap['LapTime'].total_seconds()
        self.speed_frequency = self.lap_time / len(self.lap_speed)
        self.speed_index = self.lap_speed.keys()[0]

    def start_preview(self, dt):
        self.speed_index += 1
        self.ids.spd_label.text = str(self.lap_speed[self.speed_index])

    def start_telemetry(self):
        self.ids.start_button.text = "STOP"
        self.simulation_going = True
        Clock.schedule_interval(self.start_preview, self.speed_frequency)

    def exit_back(self):
        self.manager.current = "start"

