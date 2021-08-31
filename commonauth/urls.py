from django.urls import path, re_path, include
from commonauth import views as commonauth_views



api_patterns = [
  path('tokens', commonauth_views.Token.as_view()),
  path('users', commonauth_views.User.as_view()),
  path('passwords', commonauth_views.Password.as_view()),
  # path('token', TokenObtainPairView.as_view()),
  # path('users', commonauth_views.as_view()),
  # path('logout', commonauth_views.logout),
  # path('checkAuth', commonauth_views.checkAuth),
  # path('changePass', commonauth_views.changePass),
  # path('updateInfo', commonauth_views.updateInfo),
  # path('register', commonauth_views.register),
  # path('user', commonauth_views.user),
]
