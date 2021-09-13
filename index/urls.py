from django.urls import path, re_path, include
# from apiadmin import diary
from index import views as index_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  path('moodtalk', index_views.MoodSentence.as_view()), # 推播心情小語
  path('latest', index_views.LatestDiary.as_view()), # 抓最新的兩篇日記
]
