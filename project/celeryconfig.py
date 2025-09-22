'''
Descripttion: celery配置文件
version: 
Author: shaojinxin
Date: 2021-11-19 19:22:13
LastEditors: shaojinxin shaojinxin@citorytech.com
LastEditTime: 2023-04-24 17:11:11
'''
# CELERY配置
# Broker配置，使用Redis作为消息中间件
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'django-db'  # BACKEND配置，这里使用ORM
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
DJANGO_CELERY_BEAT_TZ_AWARE = False
USE_TZ = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_QUEUES = {
    "queue_a": {
        "exchange": "queue_a",
        "exchange_type": "direct",
        "routing_key": "queue_a"
    },
    "queue_b": {
        "routing_key": "queue_b",
        "exchange_type": "direct",
        "exchange": "queue_b",
    }
}

CELERY_ROUTES = {
    'comment.tasks.update_comment_keyword_task': {'queue': 'queue_a', 'routing_key': 'queue_a_keyword'},
    'comment.tasks.sql_execute_task': {'queue': 'queue_a', 'routing_key': 'queue_a_sql'},
}
