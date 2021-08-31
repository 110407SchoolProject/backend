
import jwt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from commonauth.models import *
from django.contrib.auth.models import User

def token_auth_required(view_func):
  def wrap(request, *args, **kwargs):
    try:
      if "HTTP_AUTHORIZATION" in request.META:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = CommonUser.objects.get(username=decoded_token["username"])
        kwargs["decoded_token"] = decoded_token
        kwargs["user"] = user      
      else:
        kwargs["decoded_token"] = None
        kwargs["user"] = None  
    
    except Exception as e:
      print(e)
      return JsonResponse({"status_code": 401, "message": "Token Error"}, status=401)

    return view_func(request, *args, **kwargs)
  return wrap      

def admin_only(view_func):
  def wrap(request, *args, **kwargs):
    if "HTTP_AUTHORIZATION" in request.META:
      token = request.META.get('HTTP_AUTHORIZATION').split()[1]
    else:
      return JsonResponse({"status_code": 200, "message": "NO AUTHORIZE_KEY EXISTS"}, status=200)
    
    try:      
      decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
      # print(decoded_token)
      user = User.objects.get(username=decoded_token["username"])

      kwargs["decoded_token"] = decoded_token
      kwargs["user"] = user


      if user == None:
        raise Exception
    except Exception as e:
      print(e)
      return JsonResponse({"status_code": 401, "message": "Token Error"}, status=200)


    return view_func(request, *args, **kwargs)
  return wrap      

def permission_required(perms=[]):
  def decorator(view_func):
    def wrap(request, *args, **kwargs):
      token = request.META.get('HTTP_AUTHORIZATION').split()[1]
      try:

        permissions_confirmed = []      
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = CommonUser.objects.get(username=decoded_token["username"])
        if user == None:
          raise Exception

        for perm in perms:
          for role in user.roles.all():
            if role.has_permission(perm):
              permissions_confirmed.append(True)
              break
        
        if len(permissions_confirmed) == len(perms):
          return view_func(request, *args, **kwargs)
        else:
          raise Exception
      except Exception as e:
        print(e)
        return JsonResponse({"status_code": 401, "message": "Token Error"}, status=401)      
    return wrap
  return decorator 



def role_required(allowed_roles=[]):
  def decorator(view_func):
    def wrap(request, *args, **kwargs):
      if request.user.profile.userStatus in allowed_roles:
        return view_func(request, *args, **kwargs)
      else:
        return render(request, "dashboard/404.html")
    return wrap
  return decorator
