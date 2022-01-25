from django.urls import path, re_path, include
# from apiadmin import diary
from profileStatus import views as profileStatus_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  path('status', profileStatus_views.ProfileStatus.as_view()),
]
