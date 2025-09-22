'''
Author: shaojinxin
Date: 2022-09-14 11:01:49
LastEditTime: 2022-09-23 17:00:36
Description: 

Copyright (c) 2022 by shaojinxin/citorytech, All Rights Reserved. 
'''
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
__all__ = ['celery_app']