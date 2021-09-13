from django.urls import path, re_path, include
# from apiadmin import diary
from moodtree import views as moodtree_views

#api/diary/diarysuuid
#api/diary/diarys


api_patterns = [
  # path('diarys', diary_views.Diary.as_view()),
  re_path(r'moodtree/days', diary_views.Diary.as_view()),
  #path('users', diary_views.User.as_view()),
  #path('passwords', diary_views.Password.as_view()),
  # path('token', TokenObtainPairView.as_view()),
  # path('users', commonauth_views.as_view()),
  # path('logout', commonauth_views.logout),
  # path('checkAuth', commonauth_views.checkAuth),
  # path('changePass', commonauth_views.changePass),
  # path('updateInfo', commonauth_views.updateInfo),
  # path('register', commonauth_views.register),
  # path('user', commonauth_views.user),
]
