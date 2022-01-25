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
from moodspider import urls as moodspider_urls
from index import urls as index_urls
from moodtree import urls as moodtree_urls
from analysis import urls as analysis_urls
from bert import urls as bert_urls
from profileStatus import urls as profileStatus_urls
from passwordError import urls as passwordError_urls
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/commonauth/', include(commonauth_urls.api_patterns)),
    re_path(r'^api/diary/',include(diary_urls.api_patterns)),
    re_path(r'^api/index/',include(index_urls.api_patterns)),
    re_path(r'^api/analysis/',include(analysis_urls.api_patterns)),
    re_path(r'^api/moodtree/',include(moodtree_urls.api_patterns)),
    re_path(r'^api/moodspider/',include(moodspider_urls.api_patterns)),
    re_path(r'^api/bert/',include(bert_urls.api_patterns)),
    re_path(r'^api/status/',include(profileStatus_urls.api_patterns)),
    re_path(r'^api/passworderror/',include(passwordError_urls.api_patterns))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
