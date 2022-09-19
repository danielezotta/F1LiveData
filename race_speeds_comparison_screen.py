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
import math

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
import fastf1
import globals


Builder.load_file('race_speeds_comparison_screen.kv')


class RaceSpeedsComparisonScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lap_driver_one = None
        self.lap_driver_two = None
        self.loading_data = None

    def on_pre_enter(self, *args):
        Window.size = (1000, 800)

    def on_enter(self, *args):
        self.loading_data = True
        Clock.schedule_once(self.get_laps, 1)

    def get_laps(self, dt):
        session = fastf1.get_session(globals.year, globals.circuit_number, 'R')
        session.load(laps=True, telemetry=True, weather=True)
        self.lap_driver_one = session.laps.pick_driver(globals.driver_number).pick_fastest()
        self.lap_driver_two = session.laps.pick_driver(globals.driver2_number).pick_fastest()
        self.laps_driver_one = session.laps.pick_driver(globals.driver_number)
        self.laps_driver_two = session.laps.pick_driver(globals.driver2_number)
        self.loading_data = False
        self.ids.info_label.text = '[color=%s]%s[/color] | [color=%s]%s[/color]' % (globals.driver_color, globals.driver_name, globals.driver2_color, globals.driver2_name)

        self.driver_one_interval = (self.lap_driver_one['LapTime'].total_seconds() / self.lap_driver_one.telemetry['X'].size) * 1000
        self.driver_two_interval = (self.lap_driver_two['LapTime'].total_seconds() / self.lap_driver_two.telemetry['X'].size) * 1000

        self.load_speeds()

    def load_speeds(self):

        self.ids.stats_layout.add_widget(Label(text='', font_size='24sp'))
        self.ids.stats_layout.add_widget(Label(text='[color=#%s]%s[/color]' % (globals.driver_color, globals.driver_name), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='[color=#%s]%s[/color]' % (globals.driver2_color, globals.driver2_name), font_size='24sp', markup=True))

        self.ids.grid_layout.add_widget(Label(text='#', font_size='24sp'))
        self.ids.grid_layout.add_widget(Label(text='SpeedI1', font_size='24sp'))
        self.ids.grid_layout.add_widget(Label(text='SpeedI2', font_size='24sp'))
        self.ids.grid_layout.add_widget(Label(text='SpeedFL', font_size='24sp'))
        self.ids.grid_layout.add_widget(Label(text='SpeedST', font_size='24sp'))

        lap = 1

        speedI1_driver1_avg = 0
        speedI1_driver1_tot = 0
        speedI1_driver2_avg = 0
        speedI1_driver2_tot = 0
        speedI2_driver1_avg = 0
        speedI2_driver1_tot = 0
        speedI2_driver2_avg = 0
        speedI2_driver2_tot = 0
        speedFL_driver1_avg = 0
        speedFL_driver1_tot = 0
        speedFL_driver2_avg = 0
        speedFL_driver2_tot = 0
        speedST_driver1_avg = 0
        speedST_driver1_tot = 0
        speedST_driver2_avg = 0
        speedST_driver2_tot = 0

        for driver1_row, driver2_row in zip(self.laps_driver_one.itertuples(index=False), self.laps_driver_two.itertuples(index=False)):
            self.ids.grid_layout.add_widget(Label(text='LAP %d' % (lap), font_size='24sp'))
            self.ids.grid_layout.add_widget(Label(text='[color=%s]%s[/color]\n[color=%s]%s[/color]' % (globals.driver_color, str(driver1_row.SpeedI1), globals.driver2_color, str(driver2_row.SpeedI1)), font_size='20sp', markup=True))
            self.ids.grid_layout.add_widget(Label(text='[color=%s]%s[/color]\n[color=%s]%s[/color]' % (globals.driver_color, str(driver1_row.SpeedI2), globals.driver2_color, str(driver2_row.SpeedI2)), font_size='20sp', markup=True))
            self.ids.grid_layout.add_widget(Label(text='[color=%s]%s[/color]\n[color=%s]%s[/color]' % (globals.driver_color, str(driver1_row.SpeedFL), globals.driver2_color, str(driver2_row.SpeedFL)), font_size='20sp', markup=True))
            self.ids.grid_layout.add_widget(Label(text='[color=%s]%s[/color]\n[color=%s]%s[/color]' % (globals.driver_color, str(driver1_row.SpeedST), globals.driver2_color, str(driver2_row.SpeedST)), font_size='20sp', markup=True))
            lap += 1

            if not math.isnan(driver1_row.SpeedI1):
                speedI1_driver1_avg += driver1_row.SpeedI1
                speedI1_driver1_tot += 1
            if not math.isnan(driver2_row.SpeedI1):
                speedI1_driver2_avg += driver2_row.SpeedI1
                speedI1_driver2_tot += 1
            if not math.isnan(driver1_row.SpeedI2):
                speedI2_driver1_avg += driver1_row.SpeedI2
                speedI2_driver1_tot += 1
            if not math.isnan(driver2_row.SpeedI2):
                speedI2_driver2_avg += driver2_row.SpeedI2
                speedI2_driver2_tot += 1
            if not math.isnan(driver1_row.SpeedFL):
                speedFL_driver1_avg += driver1_row.SpeedFL
                speedFL_driver1_tot += 1
            if not math.isnan(driver2_row.SpeedFL):
                speedFL_driver2_avg += driver2_row.SpeedFL
                speedFL_driver2_tot += 1
            if not math.isnan(driver1_row.SpeedST):
                speedST_driver1_avg += driver1_row.SpeedST
                speedST_driver1_tot += 1
            if not math.isnan(driver2_row.SpeedST):
                speedST_driver2_avg += driver2_row.SpeedST
                speedST_driver2_tot += 1

        self.ids.stats_layout.add_widget(Label(text='SpeedI1 AVG', font_size='24sp'))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedI1_driver1_avg / speedI1_driver1_tot, 2)), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedI1_driver2_avg / speedI1_driver2_tot, 2)), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='SpeedI2 AVG', font_size='24sp'))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedI2_driver1_avg / speedI2_driver1_tot, 2)), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedI2_driver2_avg / speedI2_driver2_tot, 2)), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='SpeedFL AVG', font_size='24sp'))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedFL_driver1_avg / speedFL_driver1_tot, 2)), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedFL_driver2_avg / speedFL_driver2_tot, 2)), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='SpeedST AVG', font_size='24sp'))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedST_driver1_avg / speedST_driver1_tot, 2)), font_size='24sp', markup=True))
        self.ids.stats_layout.add_widget(Label(text='%s' % str(round(speedST_driver2_avg / speedST_driver2_tot, 2)), font_size='24sp', markup=True))

    def exit_back(self):
        self.ids.info_label.text = 'Loading...'
        self.ids.stats_layout.clear_widgets()
        self.ids.grid_layout.clear_widgets()
        self.manager.current = "race_speeds_comparison"
