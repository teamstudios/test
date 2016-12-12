from django.contrib.auth.models import User

from .models import ActivationProfile


class TokenAuthBackend:
    """
    Authenticate user by token(sent on email) or by sms code
    """
    def authenticate(self, username=None, token=None, code=None):
        try:
            user = User.objects.get(username=username)
            try:
                if token:
                    activation = ActivationProfile.objects.get(user=user, token=token)
                    return user
                elif code:
                    activation = ActivationProfile.objects.get(user=user, sms_key=code)
                    return user
                else:
                    return None
            except ActivationProfile.DoesNotExist:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailAuthBackend:
    """
    Authenticate user by email and password
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
