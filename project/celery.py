'''
Descripttion: 
version: 
Author: shaojinxin
Date: 2021-09-16 11:11:21
LastEditors: shaojinxin
LastEditTime: 2022-01-17 14:43:11
'''
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # 设置django环境

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY') #  使用CELERY_ 作为前缀，在settings中写配置

app.autodiscover_tasks()  # 发现任务文件每个app下的task.py

app.conf.beat_schedule ={
        'data_update_task': {
        "task": "webserver.tasks.data_update_task",
        "schedule": crontab(hour=3,minute=0),
        # "args": [3],  #参数
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))