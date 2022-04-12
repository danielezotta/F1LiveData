from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
import fastf1
import globals
import time
import threading
from threading import Thread


Builder.load_file('quali_steering_wheel_screen.kv')


class QualiSteeringWheelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lap = None
        self.lap_speed = None
        self.lap_time = None
        self.data_frequency = None
        self.simulation_going = False
        self.start_index = None
        self.rpm_engine = None
        self.gear = None
        self.interval = None
        self.end_index = None
        self.loading_data = True

    def on_enter(self, *args):
        self.loading_data = True
        self.ids.start_button.text = "LOADING ..."
        self.ids.info_label.text = '%s - %s' % (globals.driver_name, globals.circuit_name)
        Clock.schedule_once(self.get_lap, 1)
        # self.get_lap()

    def get_lap(self, dt):
        session = fastf1.get_session(2022, globals.circuit_number, 'Q')
        session.load(laps=True, telemetry=True, weather=True)
        self.lap = session.laps.pick_driver(globals.driver_number).pick_fastest()
        self.lap_speed = self.lap.telemetry['Speed']
        self.rpm_engine = self.lap.telemetry['RPM']
        self.gear = self.lap.telemetry['nGear']
        self.ids.time_label.text = str(self.lap['LapTime']).strip("0 days 00:")
        self.lap_time = self.lap['LapTime'].total_seconds()
        self.data_frequency = self.lap_time / len(self.lap_speed)
        self.start_index = self.lap_speed.keys()[0]
        self.end_index = self.lap_speed.keys()[-1]
        self.ids.start_button.text = "START"
        self.loading_data = False

    def start_preview(self, dt):
        if self.start_index < self.lap_speed.keys()[-1]:
            self.start_index += 1
            self.ids.spd_label.text = str(self.lap_speed[self.start_index])
            self.ids.rpm_label.text = str(self.rpm_engine[self.start_index])
            self.ids.gear_label.text = str(self.gear[self.start_index])
        else:
            Clock.unschedule(self.interval)
            self.ids.start_button.text = "START"
            self.simulation_going = False

    def start_telemetry(self):
        if not self.loading_data and not self.simulation_going:
            self.ids.start_button.text = "STOP"
            self.simulation_going = True
            self.interval = Clock.schedule_interval(self.start_preview, self.data_frequency)
        elif self.simulation_going:
            Clock.unschedule(self.interval)
            self.ids.start_button.text = "START"
            self.simulation_going = False

    def exit_back(self):
        self.manager.current = "quali_steering"

