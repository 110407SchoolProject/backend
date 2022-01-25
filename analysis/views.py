from re import I
import re
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
import pandas as pd
from matplotlib import font_manager
from datetime import date, datetime, time, timedelta
import numpy as np
import time

logging = logging.getLogger(__name__)
@method_decorator(csrf_exempt,name="dispatch")
class AnalysisScore(View):
    @method_decorator(token_auth_required)
        # 取得moodscore分數做平均
    def post(self,request, *args, **kwargs):
        try:
            moodscore_list = []
            total = 0
            req = json.loads(request.body)
            # days = req["days"]
            # startdate = datetime.today()
            # enddate = startdate + timedelta(days=-days)
            start = req['start']
            end = req['end']
            # 轉成datetime格式
            datetime_start = datetime.strptime(start, "%Y-%m-%d")
            datetime_end = datetime.strptime(end,"%Y-%m-%d") + timedelta(days=1)
            # 轉回String
            string_start = datetime.strftime(datetime_start, "%Y-%m-%d")
            string_end = datetime.strftime(datetime_end,"%Y-%m-%d")
            moodscore = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[string_start, string_end]).order_by('-create_date').values('moodscore')
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            for score in moodscore_list:
                total = total + score
            print(moodscore_list)
            print(total)
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
    
    # 取得總日記篇數
    @method_decorator(token_auth_required)
    def get(self, request, *args, **kwargs):
        try:
            diary_number_list = []
            diary_numbers = diary_models.objects.filter(userid = kwargs["user"]).order_by('-create_date').values('moodscore')
            print(diary_numbers)
            for i in range(len(diary_numbers)):
                diary_number_list.append(diary_numbers[i].get('moodscore'))

            res = {
                "result":"ok",
                "diary_number":len(diary_number_list)
            }

                # print(diary_number)
            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)


    #取得最新兩篇日記心情
    @method_decorator(token_auth_required)
    def put(self,request,*args, **kwargs):
        try:
            latest_2_diarys_score_list = []
            latest_2_diarys = diary_models.objects.filter(userid = kwargs["user"]).order_by('-create_date').values('moodscore')[:2]
            for i in range(len(latest_2_diarys)):
                latest_2_diarys_score_list.append(latest_2_diarys[i].get('moodscore'))
            first = latest_2_diarys_score_list[0] * 1.5
            second = latest_2_diarys_score_list[1] * 1
            total = (first + second) / 2.5

            res = {
                "result": "ok",
                "score": total
            }
            return JsonResponse(res, status = 200)

        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)
    

@method_decorator(csrf_exempt,name="dispatch")
class Analysis(View):
    @method_decorator(token_auth_required)
    # 取得moodscore分數做平均
    def get(self,request, *args, **kwargs):
        try:
            moodscore_list = []
            total = 0
            req = json.loads(request.body)
            # days = req["days"]
            # startdate = datetime.today()
            # enddate = startdate + timedelta(days=-days)
            start = req['start']
            end = req['end']
            # 轉成datetime格式
            datetime_start = datetime.strptime(start, "%Y-%m-%d")
            datetime_end = datetime.strptime(end,"%Y-%m-%d") + timedelta(days=1)
            # 轉回String
            string_start = datetime.strftime(datetime_start, "%Y-%m-%d")
            string_end = datetime.strftime(datetime_end,"%Y-%m-%d")
            moodscore = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[string_start, string_end]).order_by('-create_date').values('moodscore')
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
                "score": float(scores)
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
            # days = req["days"]
            # startdate = datetime.today()
            # enddate = startdate + timedelta(days=-days)
            start = req['start']
            end = req['end']
            # 轉成datetime格式
            datetime_start = datetime.strptime(start, "%Y-%m-%d")
            datetime_end = datetime.strptime(end,"%Y-%m-%d") + timedelta(days=1)
            # 轉回String
            string_start = datetime.strftime(datetime_start, "%Y-%m-%d")
            string_end = datetime.strftime(datetime_end,"%Y-%m-%d")
            tags = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[string_start, string_end]).order_by('-create_date').values('moodscore','tag', 'tag2', 'tag3')
            for i in range(len(tags)):
                if tags[i].get('moodscore') >=3:
                    positive_tags_list.append(tags[i].get('tag'))
                    positive_tags_list.append(tags[i].get('tag2'))
                    positive_tags_list.append(tags[i].get('tag3'))
                else:
                    negative_tags_list.append(tags[i].get('tag'))
                    negative_tags_list.append(tags[i].get('tag2'))
                    negative_tags_list.append(tags[i].get('tag3'))
            positive_most = []
            negative_most = []
            positive = Counter(positive_tags_list)
           
            #positive_most = positive.most_common(2)
            negative = Counter(negative_tags_list)
            
            #negative_most = negative.most_common(2)
            for i in range(len(positive.most_common(3))):
                positive_most.append(positive.most_common(3)[i][0])
            for j in range(len(negative.most_common(3))):
                negative_most.append(negative.most_common(3)[j][0]) 

            res = {
                "result": "ok",
                "positive_tags": positive_most,
                "negative_tags": negative_most
            }
            return JsonResponse(res, status = 200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)


    @method_decorator(token_auth_required)
    # 取得日記篇數
    def put(self, request, *args, **kwargs):
        try:
            diary_list = []
            req = json.loads(request.body)
            start = req['start']
            end = req['end']
            # 轉成datetime格式
            datetime_start = datetime.strptime(start, "%Y-%m-%d")
            datetime_end = datetime.strptime(end,"%Y-%m-%d") + timedelta(days=1)
            # 轉回String
            string_start = datetime.strftime(datetime_start, "%Y-%m-%d")
            string_end = datetime.strftime(datetime_end,"%Y-%m-%d")
            diarys = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[string_start, string_end]).order_by('-create_date').values('content')
            for i in range(len(diarys)):
                diary_list.append(diarys[i].get('content'))
            
            res = {
                "result": "ok",
                "count_diarys":len(diary_list)
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
    def post(self,request, *args, **kwargs):
        try:
            my_path = os.path.dirname(__file__)
            # print('圓餅圖' + my_path)
            colors = ['#FC6170','#FF8A47','#FFD747', '#8CEEEE','#26BFBF']
            moodscore_list  = []
            req = json.loads(request.body)
            start = req['start']
            end = req['end']
            # 轉成datetime格式
            datetime_start = datetime.strptime(start, "%Y-%m-%d")
            datetime_end = datetime.strptime(end,"%Y-%m-%d") + timedelta(days=1)
            # 轉回String
            string_start = datetime.strftime(datetime_start, "%Y-%m-%d")
            string_end = datetime.strftime(datetime_end,"%Y-%m-%d")
            #startdate = datetime.today()
            # enddate = startdate + timedelta(days=-days)
            # create_date__range=[enddate, startdate]
            moodscore = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[string_start,string_end] ).order_by('-create_date').values('moodscore')
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            if (len(moodscore_list) == 0):
                res = {
                    "result": "{}到{}無日記".format(start, end)
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
                #plt.figure(figsize=(20,16))
                fig,ax=plt.subplots(figsize=(18,18))
                pie1,c1_text,n1_text=ax.pie(percentage,autopct=lambda p:f'{p:.0f}%',radius=0.7,pctdistance=0.7,
                wedgeprops=dict(width=0.3,edgecolor='w'), colors=color_list, textprops={'color':"black","fontsize" : 12})
                for t in c1_text:
                    t.set_size(50)
                for n in n1_text:
                    n.set_size(50)
                ax.set(aspect='equal')
                plt.show()
                plt.savefig(my_path + '/piechart.png', transparent=True) #transparent=True
                time.sleep(1)
                #os.remove('/home/schoolproject/diary-app/backend/media/piechart/piechart.png')
                shutil.move('/home/schoolproject/diary-app/backend/analysis/piechart.png', '/home/schoolproject/diary-app/backend/media/piechart/piechart.png')
                image_url = "media/piechart/piechart.png"
                res = {
                    "result": "ok",
                    "pie_image_url":"{}".format(image_url)
                }
                #time.sleep(5)
                print(datetime.now())
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)


@method_decorator(csrf_exempt,name="dispatch")
class LineChart(View):
    # 繪製折線圖
    @method_decorator(token_auth_required)
    def post(self,request, *args, **kwargs):
        try:
            my_path = os.path.dirname(__file__)
            # print('長餅圖' + my_path)
            moodscore_list  = []
            title_list = []
            reverse_title_list = []
            req = json.loads(request.body)
            start = req['start']
            end = req['end']
            # 轉成datetime格式
            datetime_start = datetime.strptime(start, "%Y-%m-%d")
            datetime_end = datetime.strptime(end,"%Y-%m-%d") + timedelta(days=1)
            # 轉回String
            string_start = datetime.strftime(datetime_start, "%Y-%m-%d")
            string_end = datetime.strftime(datetime_end,"%Y-%m-%d")
            #startdate = datetime.today()
            #enddate = startdate + timedelta(days=-days)
            moodscore = diary_models.objects.filter(userid = kwargs["user"],create_date__range=[string_start, string_end]).order_by('create_date').values('moodscore')
            title = diary_models.objects.filter(userid = kwargs["user"],create_date__range=[string_start, string_end]).order_by('create_date').values('title')
            for i in range(len(moodscore)):
                moodscore_list.append(moodscore[i].get('moodscore'))
            for i in range(len(title)):
                title_list.append(title[i].get('title'))
            
            for i in range(len(title_list)-1, -1,-1):
                reverse_title_list.append(title_list[i])
            
            if (len(title_list) == 0):
                res = {
                    "result": "{}到{}無日記".format(start, end)
                }
            else:
                fontP = font_manager.FontProperties()
                fontP.set_family('SimHei.ttf')
                fontP.set_size(18)
                plt.legend(loc=0, prop=fontP)
                # ax = plt.axes()
                # ax.set_facecolor('#eafff5')
                plt.figure(figsize=(12,8))
                plt.plot(moodscore_list, color='#EAC100',marker='o',markersize=20, linewidth=5)
                #plt.grid(axis = "x",linestyle='solid', linewidth = 0.5, color='g')
                x = []
                for i in range(len(title_list)):
                    x.append(i)
                print(x)
                # plt.xticks(x, title_list,rotation=0)
                # plt.yticks([1,2,3,4,5])
                # print(title_list)
                # print(x)
                # print(moodscore_list)
                #plt.xticks(moodscore_list)
                #plt.yticks(x,title_list)
                #plt.xticks([])
                #print(title_list)
                #print(title_list)
                print(reverse_title_list)
                print(title_list)
                plt.xticks(x, reverse_title_list, fontsize=0, color='white')
                plt.yticks([1,2,3,4,5], [1,2,3,4,5],fontsize=20)
                # plt.xticks(x, title_list,fontsize=0, color='white')
                # plt.yticks([1,2,3,4,5], [1,2,3,4,5],fontsize=20)
                #plt.yticks(x,moodscore_list)
                plt.xlabel('{}篇日記(過去至現在)'.format(len(title_list)), fontsize = 30)
                plt.ylabel('心情分數', fontsize = 40)
                plt.show()
                plt.savefig(my_path + '/linechart.png', transparent=True) #transparent=True
                #time.sleep(1)
                print(datetime.now())
                shutil.move(my_path + '/linechart.png', '/home/schoolproject/diary-app/backend/media/linechart/linechart.png')
                image_url = "media/linechart/linechart.png"
                res = {
                    "result": "ok",
                    "line_image_url":"{}".format(image_url)
                }
                print(datetime.now())
                time.sleep(1)
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)