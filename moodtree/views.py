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
from moodtree import models as moodtree_models
from django.db import transaction
from diary.models import Diary as diary_models
import os
#from typing import Generator
import jieba
#import wordcloud
from wordcloud import WordCloud
import scipy.misc
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from os import path
from PIL import Image
from matplotlib import colors
import os
import shutil
from pathlib import Path


logging = logging.getLogger(__name__)

@method_decorator(csrf_exempt,name="dispatch")
class Moodtree(View):
    # 新增 diary
    @method_decorator(token_auth_required)
    def get(self,request, *args, **kwargs):
        try:
            diary_list = []
            req = json.loads(request.body)
            days = req["days"]
            diarys = diary_models.objects.filter(userid = kwargs["user"]).order_by('-create_date').values('content')[:days]
            for i in range(len(diarys)):
                diary_list.append(diarys[i].get('content'))
            path = '/home/schoolproject/diary-app/backend/moodtree/diary.txt'
            f = open(path, 'w')
            f.writelines(diary_list)
            f.close()

            text_file = open(os.path.abspath('/home/schoolproject/diary-app/backend/moodtree/diary.txt'), encoding="utf-8")
            text_list = text_file.read()

            punctuation = set()
            with open(os.path.abspath('/home/schoolproject/diary-app/backend/moodtree/punctuation_zh_tw.txt'), encoding='utf-8') as f:
                for line in f.readlines():
                    punctuation.add(line.strip())
            with open(os.path.abspath('/home/schoolproject/diary-app/backend/moodtree/punctuation_en.txt'),encoding='utf-8') as f:
                for line in f.readlines():
                    punctuation.add(line.strip())
            punctuation.add(' ')
            punctuation.add('\n')

            with open(os.path.abspath('/home/schoolproject/diary-app/backend/moodtree/stopwords_zh_tw.txt'),encoding="utf-8") as file:
                stopwords = {line.strip() for line in file}

            # word變數在jieba.cut(text_list)中迭代，找出沒有在punctuation及stopwords中出現的字，且將這些字加入到新的set中
            word_list = {word for word in jieba.cut(text_list) if word not in punctuation and word not in stopwords}
            print(word_list)
            data = dict()
            for word in word_list:
                if len(word) >=2:
                    if not data.__contains__(word):
                        data[word] = 0
                    data[word]=+1
            mask = np.array(Image.open('/home/schoolproject/diary-app/backend/moodtree/big-tree-without-root.png'))
            color_list=['#66FF66', '#ffd95c','#4ac6D7','#f5855b','#68bbb8','#e81b23']
            colormap=colors.ListedColormap(color_list)
            my_wordcloud = WordCloud(mode="RGBA", background_color="rgba(255, 255, 255, 0)", mask = mask,colormap=colormap,max_words=400,  font_path='/home/schoolproject/diary-app/backend/moodtree/MicrosoftJhengHeiRegular.ttf', width=1000, height=1000)
            my_wordcloud.generate_from_frequencies(data)
            plt.figure(figsize=(18,16))
            plt.imshow(my_wordcloud)
            plt.axis('off')
            plt.show() 
            my_wordcloud.to_file('/home/schoolproject/diary-app/backend/moodtree/wordcloud.png')
            text_file.close()

            
            shutil.move('/home/schoolproject/diary-app/backend/moodtree/wordcloud.png', '/home/schoolproject/diary-app/backend/media/wordcloud/wordcloudss.png')
    
            
            res = {
                "result": "ok"
            }
            return JsonResponse(res, status=200)
            
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)