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
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
import fastf1
import globals
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


Builder.load_file('quali_comparison_circuit_screen.kv')


class QualiComparisonCircuitScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lap_driver_one = None
        self.lap_driver_two = None
        self.loading_data = None
        self.simulation_going = None
        self.data_frequency_one = None
        self.data_frequency_two = None
        self.plot_canvas = None
        self.point1 = None
        self.point2 = None
        self.anim1 = None
        self.anim2 = None
        self.interval_one = None
        self.interval_two = None
        self.pos_index_one = None
        self.pos_index_two = None

    def on_pre_enter(self, *args):
        Window.size = (1000, 800)

    def on_enter(self, *args):
        self.loading_data = True
        self.ids.start_button.text = "LOADING ..."
        Clock.schedule_once(self.get_laps, 1)

    def on_leave(self, *args):
        self.ids.plot.remove_widget(self.plot_canvas)

    def get_laps(self, dt):
        session = fastf1.get_session(globals.year, globals.circuit_number, 'Q')
        session.load(laps=True, telemetry=True, weather=True)
        self.lap_driver_one = session.laps.pick_driver(globals.driver_number).pick_fastest()
        self.lap_driver_two = session.laps.pick_driver(globals.driver2_number).pick_fastest()
        self.ids.start_button.text = "START"
        self.loading_data = False
        self.ids.info_label.text = '%s - %s | %s - %s' % (globals.driver_name, str(self.lap_driver_one['LapTime']).replace("0 days 00:", "").replace("000", ""), str(self.lap_driver_two['LapTime']).replace("0 days 00:", "").replace("000", ""), globals.driver2_name)

        self.data_frequency_one = round(self.lap_driver_one['LapTime'].total_seconds() / self.lap_driver_one.telemetry['X'].size, 4)
        self.data_frequency_two = round(self.lap_driver_two['LapTime'].total_seconds() / self.lap_driver_two.telemetry['X'].size, 4)

        self.pos_index_one = self.lap_driver_one.telemetry['X'].keys()[0]
        self.pos_index_two = self.lap_driver_two.telemetry['X'].keys()[0]

        # create a figure with an axes
        self.fig, ax = plt.subplots(num=None, figsize=(12, 12), dpi=80, facecolor='black', edgecolor='k')
        self.fig.canvas.set_window_title('%s | %s' % (globals.driver_name, globals.driver2_name))
        self.fig.canvas.toolbar.pack_forget()
        # set equal aspect such that the circle is not shown as ellipse
        ax.set_aspect("equal")
        ax.axis('off')
        # create a point in the axes
        self.point1, = ax.plot(self.lap_driver_one.telemetry['X'][8], self.lap_driver_one.telemetry['Y'][8], marker="o", ms=14, color='Red')
        self.point2, = ax.plot(self.lap_driver_two.telemetry['X'][8], self.lap_driver_two.telemetry['Y'][8], marker="o", ms=14, color='Lightblue')

        ax.plot(self.lap_driver_one.telemetry['X'], self.lap_driver_one.telemetry['Y'], linewidth=5, zorder=0, color='white')
        ax.plot(self.lap_driver_two.telemetry['X'], self.lap_driver_two.telemetry['Y'], linewidth=5, zorder=0, color='white')

        self.driver_one_interval = (self.lap_driver_one['LapTime'].total_seconds() / self.lap_driver_one.telemetry['X'].size) * 1000
        self.driver_two_interval = (self.lap_driver_two['LapTime'].total_seconds() / self.lap_driver_two.telemetry['X'].size) * 1000
        self.plot_canvas = FigureCanvasKivyAgg(self.fig)
        self.ids.plot.add_widget(self.plot_canvas)

        # plt.show()

    def start_preview_one(self, dt):
        if self.pos_index_one < self.lap_driver_one.telemetry['X'].size:
            self.point1.set_data([self.lap_driver_one.telemetry['X'].iloc[self.pos_index_one]], [self.lap_driver_one.telemetry['Y'].iloc[self.pos_index_one]])
            self.fig.canvas.draw()
            self.pos_index_one += 1
        else:
            Clock.unschedule(self.interval_one)
            self.ids.start_button.text = "START"
            self.simulation_going = False

    def start_preview_two(self, dt):
        if self.pos_index_two < self.lap_driver_two.telemetry['X'].size:
            self.point2.set_data([self.lap_driver_two.telemetry['X'].iloc[self.pos_index_two]], [self.lap_driver_two.telemetry['Y'].iloc[self.pos_index_two]])
            self.fig.canvas.draw()
            self.pos_index_two += 1
        else:
            Clock.unschedule(self.interval_two)
            self.ids.start_button.text = "START"
            self.simulation_going = False

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
            self.interval_one = Clock.schedule_interval(self.start_preview_one, self.data_frequency_one)
            self.interval_two = Clock.schedule_interval(self.start_preview_two, self.data_frequency_two)
            # self.delta_interval = Clock.schedule_interval(self.start_delta, self.delta_frequency)
        elif self.simulation_going:
            Clock.unschedule(self.interval_one)
            Clock.unschedule(self.interval_two)
            Clock.unschedule(self.delta_interval)
            self.ids.start_button.text = "START"
            self.simulation_going = False

    def exit_back(self):
        self.manager.current = "quali_comparison"
