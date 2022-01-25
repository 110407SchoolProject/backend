from django.shortcuts import render
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
from profileStatus.models import *
from profileStatus.decorators import token_auth_required, permission_required, admin_only
from profileStatus import models as profileStatus_models
from django.db import transaction


logging = logging.getLogger(__name__)


@method_decorator(csrf_exempt,name="dispatch")
class ProfileStatus(View):
    # 新增角色狀態
    @method_decorator(token_auth_required)
    def post(self,request, *args, **kwargs):
        try:
            user = kwargs["user"]
            print(user)
            req = json.loads(request.body)
            status = req["status"][0]
            print(type(status))
            profileStatus = profileStatus_models.ProfileStatus(userid = user, status = status)
            profileStatus.save()
            res = {
                "result":"add ok"
            }
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)
    
    # 取得角色狀態
    @method_decorator(token_auth_required)
    def get(self, request, *args, **kwargs):
        try:
            status_list = []
            statuses = profileStatus_models.ProfileStatus.objects.filter(userid = kwargs["user"]).all()
            print(statuses)
            for status in statuses:
                status_list.append(status.to_json())
            if len(status_list) == 0:
                res = {
                    "result": "ok",
                    "status": []
                }
            else:
                #status_list.append(status.to_json())
                print(status_list)
                res = {
                    "result":"ok",
                    "status": status_list
                }
            # print(status.to_json())
            # print(type(status))
                
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error", str(e))
            return JsonResponse({"message": "failed", "error": str(e)}, status=500)

    # 更新角色狀態
    @method_decorator(token_auth_required)
    def put(self,request,*args,**kwargs):
        try:
            # diaryid = kwargs["diaryid"]
            # print(kwargs)
            # user = kwargs["user"]
            # print(user)
            status = profileStatus_models.ProfileStatus.objects.get(userid = kwargs["user"])
            with transaction.atomic():
                req = json.loads(request.body)
                status.status = req["status"][0]
                status.save()
            res = {
                "result": "update ok"
            }

            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)