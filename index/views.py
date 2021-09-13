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
from moodspider.models import Moodtalk as moodtalk_models
from diary.models import Diary as diray_models
from diary.decorators import token_auth_required, permission_required, admin_only
#from diary import models as diary_models
from django.db import transaction
import random


logging = logging.getLogger(__name__)


@method_decorator(csrf_exempt,name="dispatch")
class MoodSentence(View):
    # get 隨機取得心情小語
    def get(self, request, *args, **kwargs):
        try:
            sentences_list = []
            sentences = moodtalk_models.objects.all()
            for sentence in sentences:
                sentences_list.append(sentence.to_json())
            num = random.randrange(0,100)
            res = {
                "result": "ok",
                "sentence": sentences_list[num]
            }
            return JsonResponse(res, status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message": "failed","error": str(e)}, status = 500 )
    

@method_decorator(csrf_exempt,name="dispatch")
class LatestDiary(View):
    @method_decorator(token_auth_required)
    def post(self, request, *args, **kwargs):
        try:
            lastdiary_list = []
            diarys = diray_models.objects.filter(userid = kwargs["user"]).order_by('-create_date')[:2]
            #lastdiary = diarys.order_by('create_date')[len(diarys)-3:len(diarys)-1]
            #print(len(lastdiary))
            for diary in diarys:
                lastdiary_list.append(diary.all_to_json())
            res = {
                "result": "ok",
                "lastdiary": lastdiary_list
            }
            return JsonResponse(res, status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message": "failed","error": str(e)}, status = 500)