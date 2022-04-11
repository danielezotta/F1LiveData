from start_window import StartWindow
from kivy.app import App
import fastf1


class F1LiveData(App):
    def build(self):
        fastf1.Cache.enable_cache('cache')
        window = StartWindow()
        window.get_circuits()
        return window


if __name__ == '__main__':
    F1LiveData().run()

