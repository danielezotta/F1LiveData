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

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import fastf1
import globals


class QualiWheelScreen(Screen):
    kv = Builder.load_file('quali_wheel_screen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.year_select.values = ["2019", "2020", "2021", "2022"]

    def exit_back(self):
        self.manager.current = "start"

    def driver_clicked(self, value):
        globals.driver_number = int(value.split(' - ')[0])
        globals.driver_name = str(value.split(' - ')[1])

    def year_clicked(self, value):
        globals.year = int(value)
        self.get_circuits()

    def circuit_clicked(self, value):
        globals.circuit_number = int(value.split('.')[0])
        globals.circuit_name = str(value.split('. ')[1])
        self.get_drivers(globals.year, value)

    def start_clicked(self):
        if globals.circuit_number is not None and globals.driver_number is not None:
            self.manager.current = "quali_steering_data"
            print("START")

    def get_circuits(self):

        events = []

        try:
            for i in range(1, 30):
                events.append('%d. %s' % (i, fastf1.get_event(globals.year, i)['EventName']))
                print(fastf1.get_event(globals.year, i)['EventName'])
        except:
            pass

        self.ids.quali_select.values = events

    def get_drivers(self, year, event):

        drivers = []

        session = fastf1.get_session(year, globals.circuit_number, 'Q')
        session.load(telemetry=False, laps=False, weather=False)
        api_drivers = fastf1.api.driver_info(session.api_path)

        for driver in api_drivers.values():
            drivers.append('%s - %s' % (driver['RacingNumber'], driver['FullName']))

        self.ids.driver_select.values = drivers
