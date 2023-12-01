from django.conf import settings
from datetime import datetime
from jose import JWTError, jwt


class JwtManager:

    @staticmethod
    def generate_access_token(email):
        to_encode = {
            'sub': email,
            'exp': datetime.utcnow() + settings.JWT_SETTINGS.get('ACCESS_TOKEN_LIFETIME')
        }
        access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')
        return access_token

    @staticmethod
    def generate_refresh_token(email):
        to_encode = {
            'sub': email,
            'exp': datetime.utcnow() + settings.JWT_SETTINGS.get('REFRESH_TOKEN_LIFETIME')
        }
        refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')
        return refresh_token

    @staticmethod
    def get_payload(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except JWTError as jwt_err:
            print(jwt_err)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def verify_token(token):
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return True
        except JWTError as jwt_err:
            print('verify_token:', jwt_err)
            return False
        except Exception as e:
            print('verify_token:', e)
            return False

    def refresh_access_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload.get('sub')
            access_token = self.generate_access_token(email)
            return access_token

        except JWTError as jwt_err:
            print(jwt_err)
            return None
        except Exception as e:
            print(e)
            return None
