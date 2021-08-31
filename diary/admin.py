from django.contrib import admin
from diary.models import *

class DiaryAdmin(admin.ModelAdmin):
    list_display = ["diaryid","userid","title","content","tag","moodscore"]
admin.site.register(Diary,DiaryAdmin)