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
from moodtree.models import *
from moodtree.decorators import token_auth_required, permission_required, admin_only
from moodtree import models as diary_models
from django.db import transaction


logging = logging.getLogger(__name__)


@method_decorator(csrf_exempt,name="dispatch")
class Moodtree(View):
    # 新增 diary
    @method_decorator(token_auth_required)
    def post(self,request, *args, **kwargs):
        try:
            user = kwargs["user"]
            req = json.loads(request.body)
            title = req["title"]
            content = req["content"]
            tag = req["tag"]
            moodscore = req["moodscore"]
            diary = diary_models.Diary(userid = user,title = title, content = content, tag = tag, moodscore = moodscore)
            diary.save()
            res = {
                "result":"ok"
            }
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)
    
    # 刪除 diary
    @method_decorator(token_auth_required)
    def delete(self, request, *args, **kwargs):
        try:
            diary = diary_models.Diary.objects.get(diaryid = kwargs["diaryid"], userid = kwargs["user"])
            diary.delete()
            res = {
                "result":"ok"
            }
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error", str(e))
            return JsonResponse({"message": "failed", "error": str(e)}, status=500)  

    # 更新diary
    @method_decorator(token_auth_required)
    def put(self,request,*args,**kwargs):
        try:
            # diaryid = kwargs["diaryid"]
            # print(kwargs)
            # user = kwargs["user"]
            # print(user)
            diary = diary_models.Diary.objects.get(diaryid = kwargs["diaryid"], userid = kwargs["user"])
            # print(diary.moodscore)
            with transaction.atomic():
                req = json.loads(request.body)
                diary.title = req["title"]
                diary.content = req["content"]
                diary.tag  = req["tag"]
                diary.moodscore = req["moodscore"]
                diary.save()
            # diary = diary_models.Diary( title = title, content= content, tag = tag, moodscore = moodscore)
            # diary.save()
            res = {
                "result": "ok"
            }

            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)


    # 取得日記 (單一或全部)
    @method_decorator(token_auth_required)
    
    def get(self,request, *args, **kwargs):
        try:
            #user = kwargs["user"]
            # print(kwargs)
            diary_list = []
            if kwargs["diaryid"] == "":
                diarys = diary_models.Diary.objects.filter(userid=kwargs["user"]).all()
                for diary in diarys:
                    diary_list.append(diary.all_to_json())
                # 取list
            else:
                diary = diary_models.Diary.objects.get(diaryid = kwargs["diaryid"],userid = kwargs["user"])
                diary_list.append(diary.single_to_json())

            res = {
                "result": "ok",
                "diary_list": diary_list
            }
            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message": "failed","error": str(e)}, status = 500 )
