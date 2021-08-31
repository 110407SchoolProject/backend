from django.contrib.auth.hashers import check_password
from commonauth.models import CommonUser

class AuthBackend(object):
  def authenticate(self, request, username=None, password=None, **kwargs):
    try:
      user = CommonUser.objects.get(username=username)
      
      if check_password(password, user.password):
        return user
    except Exception as e:
      return None

  def get_user(self, user_id):
    try:
      return CommonUser.objects.get(pk=user_id)
    except Exception as e:
      return None
