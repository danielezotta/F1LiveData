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
        self.plot_canvas = None

    def on_pre_enter(self, *args):
        Window.size = (1000, 1000)

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

        print(self.lap_driver_one.telemetry['X'])

        # create a figure with an axes
        fig, ax = plt.subplots()
        # set equal aspect such that the circle is not shown as ellipse
        ax.set_aspect("equal")
        ax.axis('off')
        # create a point in the axes
        self.point1, = ax.plot(self.lap_driver_one.telemetry['X'][8], self.lap_driver_one.telemetry['Y'][8], marker="o")

        ax.plot(self.lap_driver_one.telemetry['X'], self.lap_driver_one.telemetry['Y'], linewidth=3, zorder=0, color='black')
        ax.plot(self.lap_driver_two.telemetry['X'], self.lap_driver_two.telemetry['Y'], linewidth=3, zorder=0, color='black')
        # self.point1, = plt.plot(self.lap_driver_one.telemetry['X'][8], self.lap_driver_one.telemetry['Y'][8], marker="o", markersize=12, markerfacecolor="green")
        # self.point2, = plt.plot(self.lap_driver_one.telemetry['X'][8], self.lap_driver_one.telemetry['Y'][8], marker="o", markersize=12, markerfacecolor="red")
        # fig = plt.figure()
        self.anim = animation.FuncAnimation(fig, self.animate, frames=len(self.lap_driver_one.telemetry['X']), interval=130, blit=True)
        # self.plot_canvas = FigureCanvasKivyAgg(plt.gcf())
        # self.ids.plot.add_widget(self.plot_canvas)
        plt.show()

    def animate(self, i):
        self.point1.set_data([self.lap_driver_one.telemetry['X'][i+8]], [self.lap_driver_one.telemetry['Y'][i+8]])
        return self.point1,
        # self.plot_canvas = FigureCanvasKivyAgg(plt.gcf())

    def start_preview(self, dt):
        if self.start_index < self.lap_speed.keys()[-1]:
            self.start_index += 1
        else:
            Clock.unschedule(self.interval)
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
            self.interval = Clock.schedule_interval(self.start_preview, self.data_frequency)
            self.delta_interval = Clock.schedule_interval(self.start_delta, self.delta_frequency)
        elif self.simulation_going:
            Clock.unschedule(self.interval)
            Clock.unschedule(self.delta_interval)
            self.ids.start_button.text = "START"
            self.simulation_going = False

    def exit_back(self):
        self.manager.current = "quali_comparison"
