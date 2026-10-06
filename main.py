import configparser
import pathlib

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from libs.config.config import AppConfig
from screens.auth.signin.ctrl import SignInScreen
from screens.auth.restore.ctrl import RestoreScreen
from screens.auth.signup.ctrl import SignUpScreen
from screens.home.ctrl import HomeScreen


class AppScreenManager(ScreenManager):
    signup_screen: SignUpScreen
    home_screen: HomeScreen
    signin_screen: SignInScreen
    restore_screen: RestoreScreen


class App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        curr_dir = str(pathlib.Path(__file__).parent.resolve())
        self.ui = Builder.load_file(curr_dir + '/ui.kv')
        self.config = AppConfig()
        # self.sm = AppScreenManager()

    def build(self):
        self.title = 'App'
        self.theme_cls.theme_style = 'Light'

        return self.ui


if __name__ == '__main__':
    App().run()
