# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 用户信息模型
class UserProfile(AbstractUser):
    mobile = models.CharField(verbose_name=u"手机号码", max_length=20, null=True, blank=True)
    gender = models.CharField(
        verbose_name=u"性别", choices=(("male", u"男"), ("female", u"女")), default="male", max_length=6)
    real_name = models.CharField(verbose_name=u"真实姓名", max_length=50, null=True, blank=True)
    identity = models.CharField(verbose_name=u"身份证号", max_length=30, null=True, blank=True)
    organization = models.CharField(verbose_name=u"学校(组织)", max_length=50, null=True, blank=True)
    year = models.CharField(verbose_name=u"入学(工作)年份", max_length=10, null=True, blank=True)
    work = models.CharField(verbose_name=u"专业(工作)", max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name=u"城市", max_length=20, null=True, blank=True)
    introduction = models.TextField(verbose_name=u"个人介绍", null=True, blank=True)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

