from django.contrib import admin
from moodspider.models import *

class MoodtalkAdmin(admin.ModelAdmin):
    list_display = ["sentence"]
admin.site.register(Moodtalk, MoodtalkAdmin)