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
from commonauth.models import CommonUser
import jwt
from django.conf import settings
from django.views import View
import datetime
from diary.models import *
from diary.decorators import token_auth_required, permission_required, admin_only
from passwordError import models as passwordError_models
from django.db import transaction


logging = logging.getLogger(__name__)


@method_decorator(csrf_exempt,name="dispatch")
class PasswordError(View):
    # 更新密碼記錄狀態
    def put(self,request,*args,**kwargs):
        try:
            status_list = []
            get_userid_list = []
            req = json.loads(request.body)
            username = req["username"]
            userid = commonauth_models.CommonUser.objects.filter(username = username).values('userid')
            print(userid)
            for userid in userid:
                get_userid_list.append(userid.get('userid'))
            print(get_userid_list[0])
            statuses = passwordError_models.PasswordError.objects.get(userid_id = get_userid_list[0])
            with transaction.atomic():
                #req = json.loads(request.body)
                statuses.error_count = req["error_count"]
                statuses.error_count_number = req["error_count_number"]
                statuses.lockstatus  = req["lockstatus"]
                statuses.save()
                pass
            res = {
                "result": "ok"
            }
            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)

    # 取得密碼記錄狀態
    def get(self,request, *args, **kwargs):
        try:
            get_userid_list = []
            status_list = []
            req = json.loads(request.body)
            username = req["username"]
            userid = commonauth_models.CommonUser.objects.filter(username = username).values('userid')
            print(userid)
            for userid in userid:
                get_userid_list.append(userid.get('userid'))
            print(type(get_userid_list[0]))
            print(get_userid_list[0])
            
            statuses = passwordError_models.PasswordError.objects.filter(userid_id=get_userid_list[0]).all()
            for status in statuses:
                status_list.append(status.to_json())
            #print(status_list)
            if (len(status_list)) == 0:
                res = {
                    "result": "ok",
                    "status":[]
                }
            else:
                res = {
                    "result": "ok",
                    "status": status_list
                }
            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message": "failed","error": str(e)}, status = 500 )


    # 新增密碼狀態
    def post(self,request,*args,**kwargs):
        try:
            req = json.loads(request.body)
            username = req["username"]
            userid = commonauth_models.CommonUser.objects.filter(username = username).values('userid')
            print(userid)
            #status = passwordError_models.PasswordError.objects.get(userid = userid)
            error_count = req["error_count"]
            error_count_number = req["error_count_number"]
            lockstatus = req["lockstatus"]
            status = passwordError_models.PasswordError(userid_id = userid, error_count = error_count, error_count_number= error_count_number,lockstatus=lockstatus)
            status.save()
            res = {
                "result":"ok"
            }
            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message": "failed","error": str(e)}, status = 500 )