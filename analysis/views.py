from django.db.models.expressions import Value
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
from diary.models import *
from diary.decorators import token_auth_required, permission_required, admin_only
from diary.models import Diary as diary_models
from django.db import transaction
import matplotlib.pyplot as plt
from collections import Counter


logging = logging.getLogger(__name__)


@method_decorator(csrf_exempt,name="dispatch")
class Analysis(View):
    @method_decorator(token_auth_required)
    # 取得moodscore分數做平均
    def get(self,request, *args, **kwargs):
        try:
            moodscore_list = []
            total = 0
            req = json.loads(request.body)
            days = req["days"]
            moodscore = diary_models.objects.filter(userid = kwargs["user"]).order_by('-create_date').values('moodscore')[:days]
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            
            for score in moodscore_list:
                total = total + score
            scores = total / len(moodscore)

            res = {
                "result":"ok",
                "score": scores
            }

            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)
    

    @method_decorator(token_auth_required)
    # 取得標籤
    def post(self, request, *args, **kwargs):
        try:
            positive_tags_list = []
            negative_tags_list = []
            req = json.loads(request.body)
            days = req["days"]
            tags = diary_models.objects.filter(userid = kwargs["user"]).order_by('-create_date').values('moodscore','tag', 'tag2', 'tag3')[:days]
            for i in range(len(tags)):
                if tags[i].get('moodscore') >=3:
                    positive_tags_list.append(tags[i].get('tag'))
                    positive_tags_list.append(tags[i].get('tag2'))
                    positive_tags_list.append(tags[i].get('tag3'))
                else:
                    negative_tags_list.append(tags[i].get('tag'))
                    negative_tags_list.append(tags[i].get('tag2'))
                    negative_tags_list.append(tags[i].get('tag3'))

            positive = Counter(positive_tags_list)
            positive_most = positive.most_common(2)
            negative = Counter(negative_tags_list)
            negative_most = negative.most_common(2)

            res = {
                "result": "ok",
                "x_most": positive_most,
                "y_most": negative_most
            }

            return JsonResponse(res, status = 200)

        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)

@method_decorator(csrf_exempt,name="dispatch")
class Chart(View):
    @method_decorator(token_auth_required)
    def get(self,request, *args, **kwargs):
        try:
            moodscore_list  = []
            req = json.loads(request.body)
            days = req['days']
            moodscore = diary_models.objects.filter(userid = kwargs["user"]).order_by('-create_date').values('moodscore')[:days]
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            print(moodscore_list)

            res = {
                "result":"ok"
                #"moodscore": moodscore_list
            }
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)