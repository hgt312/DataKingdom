# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from DjangoUeditor.models import UEditorField

from users.models import UserProfile


# 自定义上传方法
def upload_for_competition(instance, filename):
    return '/'.join(['competitions', instance.name, filename])


def upload_for_file(instance, filename):
    new_filename = instance.person.username + '.' + filename.split('.')[1]
    return '/'.join(['competitions', 'results', instance.competition.name, new_filename])


# 比赛信息模型
class Competition(models.Model):
    name = models.CharField(verbose_name=u"比赛名", max_length=50)
    is_team = models.BooleanField(verbose_name=u"是否组队参加", default=False)
    start_date = models.DateField(verbose_name=u"开始日期", null=True, blank=True)
    end_date = models.DateField(verbose_name=u"结束日期", null=True, blank=True)
    enroll_date = models.DateField(verbose_name=u"报名开始日期", null=True, blank=True)
    deadline = models.DateField(verbose_name=u"报名截止日期", null=True, blank=True)
    organization = models.CharField(verbose_name=u"学校(组织)", max_length=100, null=True, blank=True)
    image = models.ImageField(
        verbose_name=u"图片", max_length=100, upload_to=upload_for_competition, null=True, blank=True)
    exam = models.FileField(
        verbose_name=u"赛题", max_length=100, upload_to=upload_for_competition, null=True, blank=True)
    simple_intro = models.TextField(verbose_name=u"比赛简介", null=True, blank=True)
    detail = UEditorField(
        verbose_name=u"比赛详情", width=900, height=300, toolbars="full", imagePath="competitions/resources/",
        filePath="competitions/resources/", default='', blank=True)

    class Meta:
        verbose_name = u"比赛信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Competition.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except Exception as e:
            pass
        super(Competition, self).save(*args, **kwargs)


# 参赛信息模型
class AttendedPerson(models.Model):
    competition = models.ForeignKey(Competition, verbose_name=u"参与赛事")
    person = models.ForeignKey(UserProfile, verbose_name=u"参赛者（队长）")
    file = models.FileField(verbose_name=u"提交结果", null=True, blank=True, upload_to=upload_for_file)

    class Meta:
        unique_together = ("competition", "person")
        verbose_name = u"参赛信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.competition.name + '-' + self.person.username

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = AttendedPerson.objects.get(id=self.id)
            if this.file != self.file:
                this.file.delete(save=False)
        except Exception as e:
            pass
        super(AttendedPerson, self).save(*args, **kwargs)
