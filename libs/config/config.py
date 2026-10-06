from configparser import ConfigParser
from pathlib import Path

from kivy.app import App

from libs.patterns.singleton.singleton import Singleton


class AppConfig(metaclass=Singleton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__config_dir = Path(__file__).parent.resolve()
        self.config = ConfigParser()
        self.config.read(str(self.__config_dir) + '\\..\\..\\config.ini')

    def get(self, part, name):
        return self.config[part][name].replace("'", '')

    def get_user_data_dir(self):
        return App.get_running_app().user_data_dir


