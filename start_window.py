
from kivy.lang import Builder
from kivy.uix.widget import Widget
import fastf1


Builder.load_file('start_window.kv')


class StartWindow(Widget):

    def __init__(self, **kwargs):
        super().__init__()
        self.circuit_number = None
        self.driver_number = None

    def driver_clicked(self, value):
        self.driver_number = int(value.split(' - ')[0])

    def circuit_clicked(self, value):
        self.get_drivers(2022, value)
        self.circuit_number = int(value.split('.')[0])

    def start_clicked(self):
        if self.circuit_number is not None and self.driver_number is not None:
            print("START")

    def get_circuits(self):

        events = []

        try:
            for i in range(1, 30):
                events.append('%d. %s' % (i, fastf1.get_event(2022, i)['EventName']))
                print(fastf1.get_event(2022, i)['EventName'])
        except:
            print("No more races")

        self.ids.quali_select.values = events

    def get_drivers(self, year, event):

        drivers = []

        session = fastf1.get_session(year, int(event.split('.')[0]), 'Q')
        session.load(telemetry=False, laps=False, weather=False)
        api_drivers = fastf1.api.driver_info(session.api_path)

        for driver in api_drivers.values():
            drivers.append('%s - %s' % (driver['RacingNumber'], driver['FullName']))

        self.ids.driver_select.values = drivers
