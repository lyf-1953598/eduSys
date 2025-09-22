'''
Author: shaojinxin shaojinxin@citorytech.com
Date: 2022-12-12 17:23:11
LastEditors: error: git config user.name && git config user.email & please set dead value or install git
LastEditTime: 2022-12-26 12:17:25
FilePath: /metaweb_backend/apps/enroll/models.py
Description: 

Copyright (c) 2022 by shaojinxin shaojinxin@citorytech.com, All Rights Reserved. 
'''
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField
from colorfield.fields import ColorField
from django.db import models
from apps.system.models import user
import json
import datetime
# Create your models here.

# 作品来源一级分类
class fromtype(models.Model):
    name = models.CharField("来源名",max_length=128)
    def __str__(self):
        return self.name

# 作者职业
class occupation(models.Model):
    name = models.CharField("职业名称",max_length=128)
    def __str__(self):
        return self.name

# 作品类别
class category(models.Model):
    name = models.CharField("作品类别",max_length=128)
    color = ColorField(default='#FF0000',format="hexa")
    def __str__(self):
        return self.name
    
# 作品标签
class tags(models.Model):
    name = models.CharField("作品标签",max_length=128)
    def __str__(self):
        return self.name
    
# 作者
class partner(models.Model):
    name = models.CharField("作者姓名",max_length=128)
    gender = models.CharField("作者性别",max_length=32, null=True,blank=True)
    regional = models.CharField("出生地",max_length=128, null=True,blank=True)
    point  = ArrayField(models.FloatField(), size=2,verbose_name="出生地经纬度", null=True,blank=True)
    avatar = ArrayField(models.JSONField(), verbose_name="作者头像", blank=True)
    signature = models.TextField("个性签名", null=True,blank=True)
    occupation = models.ForeignKey(occupation, on_delete=models.PROTECT, verbose_name="职业名称", null=True,blank=True)
    email =  models.EmailField("邮箱", null=True,blank=True)
    phone = models.CharField("手机号",max_length=128,null=True,blank=True)
    def __str__(self):
        return self.name
# 小组
class group(models.Model):
    name = models.CharField("小组名称",max_length=128)
    leader = models.ForeignKey(partner, on_delete=models.PROTECT, null=True,verbose_name="组长")
    member = ArrayField(models.CharField(max_length=128), verbose_name="组员", blank=True)
    def __str__(self):
        return self.name
    
# 作品详情
class product(models.Model):
    fromtype = models.ForeignKey(fromtype, on_delete=models.PROTECT, null=True,blank=True,verbose_name="作品来源")
    name = models.CharField("作品名称",max_length=128)
    group = models.ForeignKey(group, on_delete=models.PROTECT, null=True,verbose_name="小组")
    regional = models.CharField("创作地点",max_length=32)
    point  = ArrayField(models.FloatField(), size=2, verbose_name="创作地点经纬度")
    category = models.ForeignKey(category, on_delete=models.PROTECT, null=True,verbose_name="作品类别")
    tags = ArrayField(models.CharField(max_length=32), verbose_name="标签(数组)", blank=True)
    description = models.TextField("作品描述", blank=True)
    def __str__(self):
        return self.name

# 作品内容
class content(models.Model):
    product = models.ForeignKey(product, on_delete=models.PROTECT, null=True,verbose_name="作品")
    stage = models.CharField(verbose_name="作品阶段",max_length=128,choices=[('start','启动'),('medium','中期'),('end','终期')],default='start')
    date = models.DateTimeField("创作时间",auto_now_add=False, null=True,blank=True)
    album = ArrayField(models.JSONField(), verbose_name="作品封面", blank=True)
    images = ArrayField(models.JSONField(), verbose_name="作品图片", blank=True)
    video = ArrayField(models.JSONField(), verbose_name="作品视频", null=True,blank=True)
    model = ArrayField(models.JSONField(), verbose_name="作品模型", null=True,blank=True)
    slide =ArrayField(models.JSONField(), verbose_name="作品ppt", null=True,blank=True)
    pdf = ArrayField(models.JSONField(), verbose_name="作品pdf", null=True,blank=True)


class social_like(models.Model):
    content = models.ForeignKey(content, on_delete=models.PROTECT, null=True,verbose_name="作品内容")
    user =  models.CharField(verbose_name="用户",max_length=128)
    date = models.DateField(verbose_name="时间",auto_now_add=True)

class social_view(models.Model):
    content = models.ForeignKey(content, on_delete=models.PROTECT, null=True,verbose_name="作品内容")
    user =  models.CharField(verbose_name="用户",max_length=128)
    date = models.DateField(verbose_name="时间",auto_now_add=True)

class social_share(models.Model):
    content = models.ForeignKey(content, on_delete=models.PROTECT, null=True,verbose_name="作品内容")
    user =  models.CharField(verbose_name="用户",max_length=128)
    date = models.DateField(verbose_name="时间",auto_now_add=True)


############新建项目表
class Project(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    longitude = models.FloatField("经度", null=False, blank=False)
    latitude = models.FloatField("纬度", null=False, blank=False)
    category = models.CharField(max_length=255, null=False, blank=False)  # 分类
    keyword = models.CharField(max_length=255, null=False, blank=False)  # 关键词
    description = models.TextField(null=False, blank=False)
    likes = models.PositiveIntegerField(default=0, null=False, blank=False)  # 点赞数，默认为 0
    image = models.CharField(max_length=255, null=False, blank=False)  # 图片路径
    video = models.CharField(max_length=255, null=True, blank=True)  # 视频路径
    file = models.FileField(max_length=255, null=True, blank=True)  # PDF文件

class UploadProject(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=False, blank=False)  # 外键关联用户表
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)  # 外键关联项目表
    time = models.DateTimeField(auto_now_add=True, null=False, blank=False)

# 点赞项目
class project_like(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=False, blank=False)  # 外键关联用户表
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)  # 外键关联项目表

# 评论项目
class project_comment(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=False, blank=False)  # 外键关联用户表
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)  # 外键关联项目表
    content = models.CharField("评论内容",max_length=500)
