from rest_framework.authentication import BaseAuthentication

from account.models import DeviceUser


class DeviceUserAuthBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = DeviceUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except DeviceUser.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return DeviceUser.objects.get(pk=user_id)
        except DeviceUser.DoesNotExist:
            return None

class DrfAuthBackend(BaseAuthentication):
    def authenticate(self, username=None, password=None):
        try:
            user = DeviceUser.objects.get(username=username)
            if user.check_password(password):
                return user, None
        except DeviceUser.DoesNotExist:

            return None