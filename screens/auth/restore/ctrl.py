from json import dumps

import certifi
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty

from libs.config.config import AppConfig
from screens.auth.ctrl import AuthBase


class RestoreScreen(AuthBase):
    restore: ObjectProperty(None)

    def restore(self):
        email = self.ids.email.text.replace(" ", '')
        if len(email) is 0:
            # @TODO Mark fields as invalid
            # self.ids.email.error = True
            pass

        restore_url = AppConfig().get(part='FIREBASE', name='restore_url') + "?key=" + self.web_api_key
        restore_payload = dumps({"email": email, "requestType": "PASSWORD_RESET"})

        UrlRequest(restore_url, req_body=restore_payload,
                   on_success=self.restore_success,
                   on_failure=self.restore_failure,
                   on_error=self.restore_error, ca_file=certifi.where())

    def restore_success(self, req, data):
        print('ook', data)
        # self.manager.current = 'login_screen'

    def restore_failure(self, req, data):
        print('ne ok', data)

    def restore_error(self, req, data):
        print('errrrr', data)
        # self.manager.current = 'login_screen'
