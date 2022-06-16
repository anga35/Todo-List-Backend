

from datetime import datetime,timedelta
from django.conf import settings
import jwt
class JWTReset:
    algorithm='HS256'
    expiry_date=1000
    def encode_reset_token(self,user_id):
        payload={
            'user_id':user_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.expiry_date)
        }
        reset_token=jwt.encode(payload,settings.SECRET_KEY,self.algorithm)
        print(reset_token)
        return reset_token

    def decode_reset_token(self,reset_token):
        try:
            decoded_data=jwt.decode(reset_token,
            settings.SECRET_KEY,algorithms=self.algorithm)
        except(jwt.DecodeError, jwt.ExpiredSignatureError):
            return None



        return decoded_data['user_id']