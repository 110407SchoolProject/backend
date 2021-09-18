from django.urls import path, re_path, include
# from apiadmin import diary
from moodtree import views as moodtree_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  # path('diarys', diary_views.Diary.as_view()),
  path('days', moodtree_views.Moodtree.as_view()),
]
