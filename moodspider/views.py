from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
import traceback
import sys
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
import json
import logging
import jwt
from django.conf import settings
from django.views import View
import datetime

from commonauth.models import *
from commonauth.decorators import token_auth_required, permission_required, admin_only

from moodspider.moodtalk.moodtalk.spiders import mood as mood
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
#from crochet import setup
import os


logging = logging.getLogger(__name__)


crawler_settings = get_project_settings()
crawler = CrawlerRunner(crawler_settings)

@method_decorator(csrf_exempt, name='dispatch')
class Moodtalk(View):
    def get(self, request, *args, **kwargs):
        configure_logging()
        runner = CrawlerRunner()
        #runner.crawl(mood.MoodSpider)
        d =runner.crawl(mood.MoodSpider)
        #d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        res = {
            "result": "ok"
        }
        return JsonResponse(res, status=200)