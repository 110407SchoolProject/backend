from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

class Moodtalk(models.Model):
    sentence = models.CharField(max_length=1024, verbose_name="心情小語")
    create_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "心情小語"
        verbose_name_plural = "心情小語"

    def __str__(self):
        return self.sentence

    def to_json(self):
        data = {
        "sentence": self.sentence
        }
        return data
    
    def save(self,*args, **kwargs):
        super(Moodtalk,self).save(*args,**kwargs)