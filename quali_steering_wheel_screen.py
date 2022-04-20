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

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import fastf1
from fastf1 import utils as fastf1utils
import globals
import time

Builder.load_file('quali_steering_wheel_screen.kv')


class QualiSteeringWheelScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lap = None
        self.lap_speed = None
        self.lap_time = None
        self.data_frequency = None
        self.simulation_going = False
        self.delta_index = None
        self.start_index = None
        self.rpm_engine = None
        self.gear = None
        self.interval = None
        self.delta_interval = None
        self.delta_frequency = None
        self.end_index = None
        self.loading_data = True
        self.prev_lap = None
        self.session_time = None
        self.lap_number = None
        self.lap_delta = None
        self.delta_time = None
        self.start_time = None
        self.end_time = None

    def on_enter(self, *args):
        self.loading_data = True
        self.ids.start_button.text = "LOADING ..."
        self.ids.info_label.text = '%s - %s' % (globals.driver_name, globals.circuit_name)
        Clock.schedule_once(self.get_lap, 1)

    def get_lap(self, dt):
        session = fastf1.get_session(globals.year, globals.circuit_number, 'Q')
        session.load(laps=True, telemetry=True, weather=True)
        laps = session.laps.pick_driver(globals.driver_number)
        accurate_laps = laps.pick_quicklaps().pick_accurate()
        self.lap = laps.pick_fastest()
        self.lap_speed = self.lap.telemetry['Speed']
        self.rpm_engine = self.lap.telemetry['RPM']
        self.gear = self.lap.telemetry['nGear']
        self.ids.time_label.text = str(self.lap['LapTime']).replace("0 days 00:", "").replace("000", "")
        self.lap_time = self.lap['LapTime'].total_seconds()
        self.session_time = self.lap['LapStartTime']
        self.lap_number = self.lap['Stint']

        for index, lap in accurate_laps[len(accurate_laps) - 2:len(accurate_laps) - 1].iterlaps():
            self.lap_delta = lap

        for i in range(int(laps['LapNumber'].keys()[0]), int(laps['LapNumber'].keys()[-1])):
            if laps['LapTime'][i].total_seconds() == self.lap_time:
                self.prev_lap = str(laps['LapStartTime'][i] - laps['LapStartTime'][i - 1]).replace("0 days 00:",
                                                                                                   "").replace("000",
                                                                                                               "")

        self.delta_time, ref_tel, compare_tel = fastf1utils.delta_time(self.lap_delta, self.lap)

        self.data_frequency = round(self.lap_time / (len(self.lap_speed)-(len(self.lap_speed) * 0.010)), 4)
        self.delta_frequency = self.lap_time / (len(self.delta_time)-(len(self.delta_time) * 0.010))
        self.delta_index = self.delta_time.keys()[0]
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
            self.end_time = time.time()
            print(self.end_time-self.start_time)

    def start_delta(self, dt):
        if self.delta_index < self.delta_time.keys()[-1]:
            self.delta_index += 1
            if self.delta_time[self.delta_index] > 0:
                self.ids.delta_label.color = [1, 0, 0, 1]
                self.ids.delta_label.text = '+ %.2f' % self.delta_time[self.delta_index]
            else:
                self.ids.delta_label.color = [0, 1, 0, 1]
                self.ids.delta_label.text = '- %.2f' % abs(self.delta_time[self.delta_index])
        else:
            Clock.unschedule(self.delta_interval)

    def start_telemetry(self):
        if not self.loading_data and not self.simulation_going:
            self.ids.start_button.text = "STOP"
            self.simulation_going = True
            self.ids.latest_lap_label.text = self.prev_lap
            self.ids.laps_session_label.text = str(self.lap_number)
            self.interval = Clock.schedule_interval(self.start_preview, self.data_frequency)
            self.delta_interval = Clock.schedule_interval(self.start_delta, self.delta_frequency)
            self.start_time = time.time()
        elif self.simulation_going:
            Clock.unschedule(self.interval)
            Clock.unschedule(self.delta_interval)
            self.ids.start_button.text = "START"
            self.simulation_going = False

    def exit_back(self):
        self.manager.current = "quali_steering"
