from django.db import models
from django.utils import timezone
# Create your models here.


# User用户表
class User(models.Model):
    # user_id = models.IntegerField(verbose_name="用户id,自增", primary_key=True)
    user_name = models.CharField(verbose_name="用户名即真实姓名", max_length=16)
    password = models.CharField(verbose_name="密码+MD5加密", max_length=20)
    telephone = models.CharField(verbose_name="电话", max_length=20, null=True)
    authority = models.CharField(verbose_name="权限", max_length=20)


# Project项目表
class Project(models.Model):
    project_id = models.IntegerField(verbose_name="项目id，自增", primary_key=True)
    project_name = models.CharField(verbose_name="项目名称", max_length=20)
    source = models.CharField(verbose_name="项目来源", max_length=30)
    contacts = models.CharField(verbose_name="对方联系人", max_length=20)
    telephone = models.CharField(verbose_name="联系电话", max_length=20)
    introduction = models.CharField(verbose_name="项目简介", max_length=256)
    time = models.DateField(verbose_name="时间", default=timezone.now)
    effective = models.IntegerField(verbose_name="是否有效", default=0)


# Report汇报表
class Report(models.Model):
    # report_id = models.IntegerField(verbose_name="汇报记录id", primary_key=True)
    report_name = models.CharField(verbose_name="汇报标题", max_length=32)
    project_id = models.IntegerField(verbose_name="所属项目id")
    reporter = models.CharField(verbose_name="汇报人", max_length=20)
    capital = models.CharField(verbose_name="资金情况", max_length=256)
    workable = models.CharField(verbose_name="落实情况", max_length=1024)
    invoice = models.CharField(verbose_name="开票情况", max_length=256)
    progress = models.CharField(verbose_name="项目进展", max_length=1024)
    supply = models.CharField(verbose_name="供货情况", max_length=1024)
    other = models.CharField(verbose_name="其它", max_length=1024)
    effective = models.IntegerField(verbose_name="是否有效", default=0)
    time = models.DateField(verbose_name="时间", default=timezone.now)


# Message留言表
class Message(models.Model):
    message_id = models.IntegerField(verbose_name="留言id", primary_key=True)
    project_id = models.IntegerField(verbose_name="项目的id")
    read = models.IntegerField(verbose_name="是否已读", default=0)
    effective = models.IntegerField(verbose_name="是否有效", default=0)
    time = models.DateField(verbose_name="时间", default=timezone.now)
    content = models.CharField(verbose_name="内容", max_length=256, null=True)


#  User_Project用户项目表
class UserProject(models.Model):
    userProject_id = models.IntegerField(verbose_name="主键", primary_key=True)
    user_name = models.CharField(verbose_name="业务员姓名", max_length=16)
    project_id = models.CharField(verbose_name="项目名称", max_length=20)


# User_str用户密文表
class UserStr(models.Model):
    userStr_id = models.IntegerField(verbose_name="主键", primary_key=True)
    user_name = models.CharField(verbose_name="用户名称", max_length=16)
    str = models.CharField(verbose_name="加密字符串", max_length=10)