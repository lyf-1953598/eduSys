'''
Author: shaojinxin shaojinxin@citorytech.com
Date: 2022-12-12 18:12:10
LastEditors: error: git config user.name && git config user.email & please set dead value or install git
LastEditTime: 2022-12-24 17:01:16
FilePath: /metaweb_backend/apps/enroll/admin.py
Description: 

Copyright (c) 2022 by shaojinxin shaojinxin@citorytech.com, All Rights Reserved. 
'''
from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(fromtype)
class fromtypeAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(partner)
class partnerAdmin(admin.ModelAdmin):
    list_display = ('name','regional','email','phone')
    
@admin.register(group)
class groupAdmin(admin.ModelAdmin):
    list_display = ('name','leader')


@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display = ('name','regional','point','description','category')

@admin.register(occupation)
class occupationAdmin(admin.ModelAdmin):
    list_display = ('id','name')


@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','color')

@admin.register(tags)
class tagsAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    
@admin.register(content)
class contentAdmin(admin.ModelAdmin):
    list_display = ('product','stage','date')