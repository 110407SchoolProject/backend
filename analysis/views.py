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
import shutil
import os
import numpy as np
import pandas as pd
from matplotlib import font_manager
from datetime import datetime, timedelta

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
            startdate = datetime.today()
            enddate = startdate + timedelta(days=-days)
            moodscore = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[enddate, startdate]).order_by('-create_date').values('moodscore')
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            for score in moodscore_list:
                total = total + score
            if total == 0:
                scores = 0
            else:
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
            startdate = datetime.today()
            enddate = startdate + timedelta(days=-days)
            tags = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[enddate, startdate]).order_by('-create_date').values('moodscore','tag', 'tag2', 'tag3')
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
class PieChart(View):
    # 繪製圓餅圖
    @method_decorator(token_auth_required)
    def get(self,request, *args, **kwargs):
        try:
            my_path = os.path.dirname(__file__)
            colors = ['#FC6170','#FF8A47','#FFD747', '#8CEEEE','#26BFBF']
            moodscore_list  = []
            req = json.loads(request.body)
            days = req['days']
            startdate = datetime.today()
            enddate = startdate + timedelta(days=-days)
            moodscore = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[enddate, startdate]).order_by('-create_date').values('moodscore')
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            if (len(moodscore_list) == 0):
                res = {
                    "result": "{}天內無日記".format(days)
                }
            else:
                duplicate = []
                percentage = []
                color_dict = {}
                j = 0
                for i in moodscore_list:
                    if(duplicate.count(i)>=1):
                        pass
                    else:
                        percentage.append((moodscore_list.count(i) / len(moodscore_list)) * 100)
                        duplicate.append(i)
                        color_dict[i] = colors[j]
                        j = j + 1
                for key, value in color_dict.items():
                    if(key == 1):
                        color_dict[1] = '#FC6170'
                    if(key == 2):
                        color_dict[2] = '#FF8A47'
                    if(key == 3):
                        color_dict[3] = '#FFD747'
                    if(key == 4):
                        color_dict[4] = '#8CEEEE'
                    if(key == 5):
                        color_dict[5] = '#26BFBF'
                color_list = [color for color in color_dict.values()]
                fig,ax=plt.subplots(figsize=(6,6))
                pie1,c1_text,n1_text=ax.pie(percentage,autopct=lambda p:f'{p:.0f}%',radius=0.7,pctdistance=0.7,
                wedgeprops=dict(width=0.3,edgecolor='w'), colors=color_list, textprops={'color':"black", 'fontsize':20})
                for t in c1_text:
                    t.set_size(13)
                for n in n1_text:
                    n.set_size(13)
                ax.set(aspect='equal')
                plt.show()
                plt.savefig(my_path + '/piechart.png', transparent=True) #transparent=True
                shutil.move('/home/schoolproject/diary-app/backend/analysis/piechart.png', '/home/schoolproject/diary-app/backend/media/analysis/piechart/piechart.png')
                res = {
                    "result":"ok"
                }
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)

@method_decorator(csrf_exempt,name="dispatch")
class LineChart(View):
    # 繪製折線圖
    @method_decorator(token_auth_required)
    def get(self,request, *args, **kwargs):
        try:
            my_path = os.path.dirname(__file__)
            moodscore_list  = []
            title_list = []
            req = json.loads(request.body)
            days = req['days']
            startdate = datetime.today()
            enddate = startdate + timedelta(days=-days)
            moodscore = diary_models.objects.filter(userid = kwargs["user"],create_date__range=[enddate, startdate]).order_by('-create_date').values('moodscore')
            title = diary_models.objects.filter(userid = kwargs["user"],create_date__range=[enddate, startdate]).order_by('-create_date').values('title')
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            for i in range(len(title)):
                title_list.append(title[i].get('title'))
            if (len(title_list) or len(moodscore_list) == 0):
                res = {
                    "result": "{}天內無日記".format(days)
                }
            else:
                #plt.subplot(1,3,3)
                fontP = font_manager.FontProperties()
                fontP.set_family('SimHei.ttf')
                fontP.set_size(14)
                plt.legend(loc=0, prop=fontP)
                ax = plt.axes()
                ax.set_facecolor("orange")
                plt.plot(title_list,moodscore_list, color='red',marker='*')
                plt.grid(axis='y',linestyle='dotted', color='b')
                x = []
                for i in range(len(title_list)):
                    x.append(i)
                plt.xticks(x, title_list,rotation=45)
                plt.yticks([1,2,3,4,5])
                plt.show()
                plt.savefig(my_path + '/linechart.png') #transparent=True
                shutil.move(my_path + '/linechart.png', '/home/schoolproject/diary-app/backend/media/analysis/linechart/linechart.png')
                res = {
                    "result":"ok"
                }
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)
