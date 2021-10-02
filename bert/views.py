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
from datetime import datetime, timedelta
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Dropout, Input, Dropout, GlobalMaxPooling1D
from transformers import TFBertModel,BertTokenizer
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

logging = logging.getLogger(__name__)

@method_decorator(csrf_exempt,name="dispatch")
class Bert(View):
    # 日記選擇性預測
    @method_decorator(token_auth_required)
    def post(self,request, *args, **kwargs):
        try:
            content_list = []
            score_list = []
            user = kwargs["user"]
            req = json.loads(request.body)
            content = req["content"]
            content_list = [content]
            bert_model = TFBertModel.from_pretrained("bert-base-chinese")
            bert_tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
            path = os.path.dirname(__file__)
            # 製作 input
            max_length = len(content)
            input_ids = layers.Input(shape=(max_length,), dtype=tf.int64)
            token_type_ids = layers.Input(shape=(max_length,), dtype=tf.int64)
            attention_mask = layers.Input(shape=(max_length,), dtype=tf.int64)
            embedding = bert_model(input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)[0]

            # BERT 模型後的輸出部分架構（可自行修改設計）
            X = GlobalMaxPooling1D()(embedding)
            X = Dense(128, activation='relu')(X)
            X = Dropout(0.05)(X)
            output = Dense(1, activation='sigmoid', name='output')(X)

            # 使用 tf.keras.Model() 建立模型
            model = tf.keras.Model(
                inputs=[input_ids, token_type_ids, attention_mask],
                outputs=output
            )
            # Restore the weights
            model.load_weights(path + '/my_model.h5')
            #X_our = df_test[['content']]
            encoded_inputs_test_our = bert_tokenizer(content_list, padding=True, truncation=True, max_length=max_length, return_tensors="tf")
            encoded_X_our = [encoded_inputs_test_our['input_ids'], encoded_inputs_test_our['token_type_ids'], encoded_inputs_test_our['attention_mask']]
            y_train_pred = model.predict(encoded_X_our,)
            y_train_pred_class = np.where(y_train_pred > 0.5, 1,0)
            for i in range(len(y_train_pred_class)):
                score_list.append(y_train_pred_class.item(i)) # get int value
        
            res = {
                "result":"ok",
                "score": score_list
            }
            return JsonResponse(res,status=200)

        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message":"failed","error":str(e)}, status=500)
    
    # 最新的兩篇日記預測心情
    @method_decorator(token_auth_required)
    def get(self,request, *args, **kwargs):
        try:
            content_list = []
            content_length_list = []
            score_list = []
            days = 2
            startdate = datetime.today()
            enddate = startdate + timedelta(days=-days)
            contents = diary_models.objects.filter(userid = kwargs["user"], create_date__range=[enddate, startdate]).order_by('-create_date').values('content')
            for content in contents:
                content_length_list.append(len(content['content']))
                content_list.append(content['content'])
            if(content_list == []):
                score_list = []
            else:
                bert_model = TFBertModel.from_pretrained("bert-base-chinese")
                bert_tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
                path = os.path.dirname(__file__)
                # 製作 input
                max_length = max(content_length_list)
                input_ids = layers.Input(shape=(max_length,), dtype=tf.int64)
                token_type_ids = layers.Input(shape=(max_length,), dtype=tf.int64)
                attention_mask = layers.Input(shape=(max_length,), dtype=tf.int64)
                embedding = bert_model(input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)[0]

                # BERT 模型後的輸出部分架構（可自行修改設計）
                X = GlobalMaxPooling1D()(embedding)
                X = Dense(128, activation='relu')(X)
                X = Dropout(0.05)(X)
                output = Dense(1, activation='sigmoid', name='output')(X)
                # 使用 tf.keras.Model() 建立模型
                model = tf.keras.Model(
                    inputs=[input_ids, token_type_ids, attention_mask],
                    outputs=output
                )
                # Restore the weights
                model.load_weights(path + '/my_model.h5')
                encoded_inputs_test_our = bert_tokenizer(content_list, padding=True, truncation=True, max_length=max_length, return_tensors="tf")
                encoded_X_our = [encoded_inputs_test_our['input_ids'], encoded_inputs_test_our['token_type_ids'], encoded_inputs_test_our['attention_mask']]
                y_train_pred = model.predict(encoded_X_our,)
                y_train_pred_class = np.where(y_train_pred > 0.5, 1,0)
                for i in range(len(y_train_pred_class)):
                    score_list.append(y_train_pred_class.item(i)) # get int value
                if(score_list.count(1) > score_list.count(0)):
                    score_list = [1]
                elif(score_list.count(1) == score_list.count(0)):
                    score_list = score_list[-1]
                else:
                    score_list = [0]
            res = {
                "result":"ok",
                "score": score_list
            }
            return JsonResponse(res,status=200)
        except Exception as e:
            traceback.print_exc()
            print("error",str(e))
            return JsonResponse({"message": "failed","error": str(e)}, status = 500 )