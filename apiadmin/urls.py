"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from commonauth import urls as commonauth_urls
from diary import urls as diary_urls
import index
from moodspider import urls as moodspider_urls
from index import urls as index_urls

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/commonauth/', include(commonauth_urls.api_patterns)),
    re_path(r'^api/diary/',include(diary_urls.api_patterns)),
    re_path(r'^api/index/',include(index_urls.api_patterns)),
    #re_path(r'^api/analysis/',include(diary_urls.api_patterns)),
    #re_path(r'^api/moodtree/',include(diary_urls.api_patterns)),
    re_path(r'^api/moodspider/',include(moodspider_urls.api_patterns)),

]
