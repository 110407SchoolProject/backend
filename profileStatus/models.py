from django.utils import timezone
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import uuid
from commonauth import models as commonauth_models
from profileStatus.views import ProfileStatus

class ProfileStatus(models.Model):
    status = models.IntegerField(verbose_name="狀態")
    userid = models.ForeignKey(commonauth_models.CommonUser, on_delete=models.CASCADE,null=True,verbose_name="使用者ID")
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "狀態"

    def __str__(self):
        return "123"

    def to_json(self):
        data = {
        "status": self.status,
        # "create_date": self.create_date,
        # "last_modified": self.last_modified
        }
        return data
    
    
    def save(self,*args, **kwargs):
        super(ProfileStatus,self).save(*args,**kwargs)