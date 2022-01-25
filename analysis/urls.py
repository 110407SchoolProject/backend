from django.urls import path, re_path, include
# from apiadmin import diary
from analysis import views as analysis_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  re_path(r'analysisscore/days', analysis_views.AnalysisScore.as_view()),
  re_path(r'analysis/days', analysis_views.Analysis.as_view()),
  re_path(r'piechart/days', analysis_views.PieChart.as_view()),
  re_path(r'linechart/days', analysis_views.LineChart.as_view()),
]