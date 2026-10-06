import json

from certifi import where
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty

from libs.config.config import AppConfig
from screens.auth.ctrl import AuthBase
from screens.common.ctrl import CommonScreen


class SignUpScreen(AuthBase):
    signup: ObjectProperty(None)

    def signup(self):
        email = self.ids.email.text.replace(" ", '')
        password = self.ids.password.text.replace(" ", '')

        if len(email) is 0 or len(password) is 0:
            # @TODO Mark fields as invalid
            # self.ids.email.error = True
            pass

        signup_url = AppConfig().get(part='FIREBASE', name='signup_url') + "?key=" + self.web_api_key
        signup_payload = json.dumps(
            {
                "email": email,
                "password": password,
                "returnSecureToken": "true"
            })

        UrlRequest(signup_url, req_body=signup_payload,
                   on_success=self.signup_success,
                   on_failure=self.signup_failure,
                   on_error=self.signup_error, ca_file=where())


    def signup_success(self, req, data):
        self.refresh_token = data['refreshToken']
        self.localId = data['localId']
        self.idToken = data['idToken']

        if self.require_email_verification:
            self.send_verification_email(data['email'])
            self.ids.screen_manager.current = 'signin_screen'

        else:
            self.save_refresh_token(self.refresh_token)
            self.login_state = 'in'
            self.login_success = True
        self.manager.current = 'home_screen'

    def signup_failure(self, req, data):
        print('ne ok')

    def signup_error(self, req, data):
        print('errrrr')
