from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import uuid
from commonauth import models as commonauth_models

class Diary(models.Model):
    diaryid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False,verbose_name="日記ID")
    userid = models.ForeignKey(commonauth_models.CommonUser, on_delete=models.CASCADE,null=True,verbose_name="使用者ID")
    title = models.CharField(max_length=128, verbose_name="日記標題")
    content = models.CharField(max_length=1024, verbose_name="日記內容")
    tag = models.CharField(max_length=50,verbose_name="標籤")
    moodscore = models.IntegerField(verbose_name="心情分數")

    create_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "日記"
        verbose_name_plural = "日記"

    def __str__(self):
        return "123"

    def single_to_json(self):
        data = {
        # "diaryid": self.diaryid,
        #"userid":self.userid,
        "title": self.title,
        "content": self.content,
        "tag": self.tag,
        "moodscore": self.moodscore
        }
        return data
    
    def all_to_json(self):
        data = {
        "diaryid": self.diaryid,
        "title": self.title,
        "content": self.content,
        "tag": self.tag,
        "moodscore": self.moodscore
        }
        return data
    
    def save(self,*args, **kwargs):
        super(Diary,self).save(*args,**kwargs)
