from django.urls import path, re_path, include
# from apiadmin import diary
from analysis import views as analysis_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  re_path(r'analysis/days', analysis_views.Analysis.as_view()),
  path(r'chart/days', analysis_views.Chart.as_view()),
]
