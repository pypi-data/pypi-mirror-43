#coding=utf-8
import datetime
from django.db import models

SSO_TOKEN_EXPIRE = 60 * 60 * 24 #1天

class Consumer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    server_host = models.CharField("服务器ip地址和端口", max_length=255, null=True, blank=True)
    user_appname = models.CharField("用户app名称", max_length=255, null=True, blank=True)
    user_modelname = models.CharField("用户model名称", max_length=255, null=True, blank=True)
    private_key = models.CharField(max_length=600)
    public_key = models.CharField(max_length=600)

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = "t_sso_consumer"

class Token(models.Model):
    consumer = models.ForeignKey(Consumer,to_field="id")
    username = models.CharField("用户名", max_length=255)
    request_token = models.CharField("请求token",max_length=600,null=True,blank=True)
    access_token = models.CharField("ͨ通过token",max_length=600,null=True,blank=True)
    timestamp = models.DateTimeField("",auto_now_add=True)
    
    def refresh(self):
        self.timestamp = datetime.datetime.now()
        self.save()
    
    class Meta:
        db_table = "t_sso_token"