from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
import traceback
import sys
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
import json
import logging
import jwt
from django.conf import settings
from django.views import View
import datetime

from commonauth.models import *
from commonauth.decorators import token_auth_required, permission_required, admin_only
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import MinimumLengthValidator
import re


logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class User(View): 
  # add user
  def post(self, request, *args, **kargs):  
    try:
      req = json.loads(request.body)
      username = req['username']
      password = req['password']
      truename = req['truename']
      nickname = req['nickname']
      gender = req['gender']
      birthday = req['birthday']
      
      # validate Email
      try:
          validate_email(username)
      except ValidationError as e:
        return JsonResponse({"message": "failed", "error": str(e)}, status=500)

      # validate password
      str_password = str(password)
      if str_password.isdigit():
            return JsonResponse({"message": "failed", "error": "至少包含一個英文字母或特殊字元"}, status=500)
      elif len(str_password) < 8:
            return JsonResponse({"message": "failed", "error": "密碼長度不可小於8位"}, status=500)
      else:
          # 實作models.py當中的CommonUser將資料存入資料庫
          user = CommonUser(username=username, password=password,truename = truename, nickname = nickname, gender = gender, birthday = birthday)
          user.save()
      res = {
        "result": "ok",
      }
      return JsonResponse(res, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)    

  # update user
  @method_decorator(token_auth_required)
  def put(self, request, *args, **kargs):  
    try:
      user = kargs["user"]
      req = json.loads(request.body)
      password = req['password']
      truename = req['truename']
      nickname = req['nickname']
      gender = req['gender']
      birthday = req['birthday']
      user.password = password
      user.truename = truename
      user.nickname = nickname
      user.gender = gender
      user.birthday = birthday
      user.save()
      res = {
        "result": "ok",
      }
      return JsonResponse(res, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)  

  # delete user
  @method_decorator(token_auth_required)
  def delete(self, request, *args, **kwargs):  
    try:
      user = kwargs["user"]
      user.delete()
      res = {
        "result": "ok",
      }
      return JsonResponse(res, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)  

  # get user
  @method_decorator(token_auth_required)
  def get(self, request, *args, **kargs):  
    try:
      user = kargs["user"]
      res = {
        "result": "ok",
        "user": user.to_json()
      }
      return JsonResponse(res, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)   

@method_decorator(csrf_exempt, name='dispatch')
class Token(View): 
  # get_token  & 登入
  def post(self, request, *args, **kargs):  
    try:
      req = json.loads(request.body)    
      username = req['username']
      password = req['password']
      user = auth.authenticate(request, username=username, password=password)
      print()    
      if user is None:
        result = {"token": ""}
      else:
        token = jwt.encode({"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=12*60*60)}, settings.SECRET_KEY, algorithm='HS256')
        result = {"token": token.decode('utf-8')}

      return JsonResponse(result, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)   

  # get_user_token_by admin token
  @method_decorator(admin_only)   
  def put(self, request, *args, **kargs):  
    try:
      req = json.loads(request.body)    
      username = req['username']
      user = CommonUser.objects.filter(username=username).first()      
      if user == None:
        result = {"token": ""}
      else:
        token = jwt.encode({"username": username}, settings.SECRET_KEY, algorithm='HS256')
        result = {"token": token.decode('utf-8')}

      return JsonResponse(result, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)   

  # check token valid
  @method_decorator(token_auth_required)    
  def get(self, request, *args, **kargs):
    try:
      user = None
      if kargs["user"] != None:
        user = kargs["user"].to_json()
      res = {
        "result": "ok",
        "user": user
      }
      return JsonResponse(res, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)   


# change password
@method_decorator(csrf_exempt, name='dispatch')
class Password(View): 
  @method_decorator(token_auth_required)  
  def post(self, request, *args, **kargs):  
    try:
      req = json.loads(request.body)  
      user = kargs["user"]  
      user.password = req['password']
      user.save()
      result = user.to_json()
      return JsonResponse(result, status=200)
      
    except Exception as e:
      traceback.print_exc()
      print("error", str(e))
      return JsonResponse({"message": "failed", "error": str(e)}, status=500)  


