from mimetypes import init
from re import U
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import base36_to_int, int_to_base36
from django.utils.crypto import constant_time_compare, salted_hmac
from datetime import datetime, time
from django.conf import settings
from requests import request

class CustomPasswordReset(PasswordResetTokenGenerator):

    limit=300
    
    
    def __init__(self):
        super().__init__()
    
    def make_token(self, user) -> str:
        token=super().make_token(user)
        user.ot_token=token
        return token


    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
            # RemovedInDjango40Warning.
            legacy_token = len(ts_b36) < 4
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            # RemovedInDjango40Warning: when the deprecation ends, replace
            # with:
            #   return False
            if not constant_time_compare(
                self._make_token_with_timestamp(user, ts, legacy=True),
                token,
            ):
                return False

        # RemovedInDjango40Warning: convert days to seconds and round to
        # midnight (server time) for pre-Django 3.1 tokens.
        now = self._now()
        if legacy_token:
            ts *= 24 * 60 * 60
            ts += int((now - datetime.combine(now.date(), time.min)).total_seconds())
        # Check the timestamp is within limit.
        if(self.limit == None):
            if (self._num_seconds(now) - ts) > settings.PASSWORD_RESET_TIMEOUT:
                return False
        else:
            
            if (self._num_seconds(now) - ts) > self.limit:
                return False


        if(not user.ot_token==token):
            print("booob")
            user.ot_token_set_expire()
            return False

        return True

