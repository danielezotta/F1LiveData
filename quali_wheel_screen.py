from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import fastf1
import globals


class QualiWheelScreen(Screen):
    kv = Builder.load_file('quali_wheel_screen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_circuits()

    def exit_back(self):
        self.manager.current = "start"

    def driver_clicked(self, value):
        globals.driver_number = int(value.split(' - ')[0])
        globals.driver_name = str(value.split(' - ')[1])

    def circuit_clicked(self, value):
        self.get_drivers(2022, value)
        globals.circuit_number = int(value.split('.')[0])
        globals.circuit_name = str(value.split('. ')[1])

    def start_clicked(self):
        if globals.circuit_number is not None and globals.driver_number is not None:
            self.manager.current = "quali_steering_data"
            print("START")

    def get_circuits(self):

        events = []

        try:
            for i in range(1, 30):
                events.append('%d. %s' % (i, fastf1.get_event(2022, i)['EventName']))
                print(fastf1.get_event(2022, i)['EventName'])
        except:
            pass

        self.ids.quali_select.values = events

    def get_drivers(self, year, event):

        drivers = []

        session = fastf1.get_session(year, int(event.split('.')[0]), 'Q')
        session.load(telemetry=False, laps=False, weather=False)
        api_drivers = fastf1.api.driver_info(session.api_path)

        for driver in api_drivers.values():
            drivers.append('%s - %s' % (driver['RacingNumber'], driver['FullName']))

        self.ids.driver_select.values = drivers
