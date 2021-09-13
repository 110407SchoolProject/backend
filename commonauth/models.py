from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class CommonUser(models.Model):
  userid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False,verbose_name="使用者ID")
  username = models.EmailField(max_length=128,unique=True,verbose_name="帳號(信箱)")
  truename = models.CharField(max_length=100, default=None, blank=True, null=True, verbose_name="姓名")
  nickname = models.CharField(max_length=128, default=None, blank=True,null=True, verbose_name="暱稱")
  password = models.CharField(max_length=128, verbose_name="密碼")
  birthday = models.DateField(max_length=128, default=None, blank=True, null=True, verbose_name="生日")
  gender = models.CharField(max_length=5, verbose_name="性別")

  create_date = models.DateField(auto_now_add=True)
  last_modified = models.DateField(auto_now=True)

  class Meta:
    ordering = ["username"]
    verbose_name = "使用者帳號"
    verbose_name_plural = "使用者帳號"

  def __str__(self):
    return self.username

  def to_json(self):
    data = {
      "userid":self.userid,
      "username": self.username,
      "password": self.password,
      "truename": self.truename,
      "nickname": self.nickname,
      "gender": self.gender,
      "birthday": self.birthday
    }
    return data

  def save(self, *args, **kwargs):
    try:
      # if no such user, raise exception
      user = CommonUser.objects.get(username=self.username)

      #find existing user, check password is changed or not
      if self.password != user.password:
        self.password = make_password(self.password)           
      super(CommonUser, self).save(*args, **kwargs)
    except:
      # run add new user
      self.password = make_password(self.password)  
      super(CommonUser, self).save(*args, **kwargs)          


