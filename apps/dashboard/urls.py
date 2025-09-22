'''
Author: shaojinxin shaojinxin@citorytech.com
Date: 2022-12-12 17:00:19
LastEditors: error: git config user.name && git config user.email & please set dead value or install git
LastEditTime: 2022-12-26 12:36:17
FilePath: /metaweb_backend/apps/dashboard/urls.py
Description: 

Copyright (c) 2022 by shaojinxin shaojinxin@citorytech.com, All Rights Reserved. 
'''
from django.urls import path

from .views import *

urlpatterns = [
    path('social/share', content_social_share.as_view(), name='content_social_share'),
    path('social/view', content_social_view.as_view(), name='content_social_view'),
    path('social/like', content_social_like.as_view(), name='content_social_like'),
    path('detail/content', get_content_detail.as_view(), name='get_content_detail'),
    path('list/content', list_content.as_view(), name='list_content'),
]