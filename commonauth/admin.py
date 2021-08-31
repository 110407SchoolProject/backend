from django.contrib import admin
from commonauth.models import *

class CommonUserAdmin(admin.ModelAdmin):
    list_display = ['userid','username','truename','password','birthday','gender']

admin.site.register(CommonUser, CommonUserAdmin)
