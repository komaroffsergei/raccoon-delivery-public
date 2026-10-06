import os
from json import dumps
from pathlib import Path

import certifi
from kivy.factory import Factory
from kivy.network.urlrequest import UrlRequest
from kivy.properties import BooleanProperty, StringProperty
from kivymd.toast import toast

from libs.config.config import AppConfig
from screens.common.ctrl import CommonScreen


class AuthBase(CommonScreen):
    web_api_key = StringProperty()  # From Settings tab in Firebase project

    # Firebase Authentication Credentials - what developers want to retrieve
    refresh_token = ""
    localId = ""
    idToken = ""

    # Properties used to send events to update some parts of the UI
    login_success = BooleanProperty(False)  # Called upon successful sign in
    login_state = StringProperty("")
    sign_up_msg = StringProperty()
    email_exists = BooleanProperty(False)
    email_not_found = BooleanProperty(False)
    remember_user = BooleanProperty(True)
    require_email_verification = BooleanProperty(True)

    debug = False
    # popup = Factory.LoadingPopup()
    current_folder = Path(__file__).parent.resolve()
    # popup.background = str(current_folder) + "/../../assets/img.png"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.refresh_token_file = AppConfig().get_user_data_dir() + "/refresh_token.txt"
        self.web_api_key = AppConfig().get(part='FIREBASE', name='web_api_key')

    def save_refresh_token(self, refresh_token):
        with open(self.refresh_token_file, "w") as f:
            f.write(refresh_token)

    def load_refresh_token(self):
        with open(self.refresh_token_file, "r") as f:
            self.refresh_token = f.read()

    def on_web_api_key(self, *args):
        if self.remember_user:
            print("REMEMBER USER IS TRUE")
            if os.path.exists(self.refresh_token_file):
                self.load_saved_account()

    def load_saved_account(self):
        """Uses the refresh token to get the user's idToken and localId by
        sending it as a request to Google/Firebase's REST API.

        Called immediately when a web_api_key is set and if the refresh token
        file exists.
        """
        self.load_refresh_token()
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api_key
        refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
        UrlRequest(refresh_url, req_body=refresh_payload,
                   on_success=self.successful_account_load,
                   on_failure=self.failed_account_load,
                   on_error=self.failed_account_load, ca_file=certifi.where())

    def successful_account_load(self, urlrequest, loaded_data):
        self.idToken = loaded_data['id_token']
        self.localId = loaded_data['user_id']
        self.login_state = 'in'
        self.login_success = True
        self.manager.current = 'home_screen'

    def failed_account_load(self, *args):
        self.hide_loading_screen()

    def sign_out(self):
        self.localId = ''
        self.idToken = ''
        self.clear_refresh_token_file()
        self.ids.screen_manager.current = 'welcome_screen'

    def clear_refresh_token_file(self):
        with open(self.refresh_token_file, 'w') as f:
            f.write('')

    def display_loading_screen(self, *args):
        pass
        # self.popup.open()

    def hide_loading_screen(self, *args):
        pass
        # self.popup.dismiss()

    def check_if_user_verified_email(self):
        """If :populate_realtime_db_with_id: is True, a verified=True record will
        be placed in this user's record.
        """

        if self.debug:
            print("Attempting to check if the user signed in has verified their email")
        check_email_verification_url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" + self.web_api_key
        check_email_verification_data = dumps(
            {"idToken": self.idToken})

        UrlRequest(check_email_verification_url, req_body=check_email_verification_data,
                   on_success=self.got_verification_info,
                   on_failure=self.could_not_get_verification_info,
                   on_error=self.could_not_get_verification_info,
                   ca_file=certifi.where())

    def could_not_get_verification_info(self, request, result):
        self.hide_loading_screen()
        toast("Failed to check email verification status.")

    def got_verification_info(self, request, result):
        if result['users'][0]['emailVerified']:
            self.login_state = 'in'
            self.login_success = True
        else:
            toast("Your email is not verified yet.\n Please check your email.")
