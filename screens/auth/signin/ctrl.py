import json

from certifi import where
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty

from libs.config.config import AppConfig
from screens.auth.ctrl import AuthBase


class SignInScreen(AuthBase):
    login: ObjectProperty(None)
    on_pre_enter: ObjectProperty(None)

    def on_pre_enter(self):
        print('working')

    def signin(self):
        email = self.ids.email.text.replace(" ", '')
        password = self.ids.password.text.replace(" ", '')

        signin_url = AppConfig().get(part='FIREBASE', name='signin_url') + "?key=" + self.web_api_key
        sign_in_payload = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True})

        UrlRequest(signin_url, req_body=sign_in_payload,
                   on_success=self.signin_success,
                   on_failure=self.signin_failure,
                   on_error=self.signin_error, ca_file=where())

    def signin_success(self, req, data):
        self.refresh_token = data['refreshToken']
        self.localId = data['localId']
        self.idToken = data['idToken']
        self.save_refresh_token(self.refresh_token)

        if self.require_email_verification:
            self.check_if_user_verified_email()
        else:
            self.login_state = 'in'
            self.login_success = True

        self.manager.current = 'home_screen'

    def signin_failure(self, req, data):
        print('ne ok')

    def signin_error(self, req, data):
        print('errrrr')
        # self.manager.current = 'login_screen'
