from django.utils import timezone
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import uuid
from commonauth import models as commonauth_models

class PasswordError(models.Model):
    userid = models.ForeignKey(commonauth_models.CommonUser, on_delete=models.CASCADE,null=True,verbose_name="使用者ID")
    error_count = models.IntegerField(verbose_name="嘗試次數")
    error_count_number = models.IntegerField(verbose_name="開鎖前被鎖定次數")
    lockstatus = models.IntegerField(verbose_name="鎖定狀態")

    class Meta:
        verbose_name = "密碼鎖定紀錄"
        verbose_name_plural = "密碼鎖定紀錄"

    def __str__(self):
        return "123"


    def to_json(self):
        data = {
            "error_count": self.error_count,
            "error_count_number": self.error_count_number,
            "lockstatus": self.lockstatus
        }
        return data
        
    def save(self,*args, **kwargs):
        super(PasswordError,self).save(*args,**kwargs)