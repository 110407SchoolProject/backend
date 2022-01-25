from django.urls import path, re_path, include

#from backend import bert
# from apiadmin import diary
from bert import views as bert_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  path('content', bert_views.Bert.as_view()),
  path('create', bert_views.Create.as_view()),
  #path('mood/', bert_views.Bert.as_view()),
]
