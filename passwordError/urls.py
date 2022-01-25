from django.urls import path, re_path, include
# from apiadmin import diary
from passwordError import views as passwordError_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  # path('diarys', diary_views.Diary.as_view()),
  path('passworderror', passwordError_views.PasswordError.as_view()),
]
