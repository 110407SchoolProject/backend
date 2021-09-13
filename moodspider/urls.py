# from _typeshed import SupportsDivMod
from django.urls import path, re_path, include
# from apiadmin import diary
from moodspider import views as moodspider_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  re_path(r'moodspider', moodspider_views.Moodtalk.as_view()),
]
