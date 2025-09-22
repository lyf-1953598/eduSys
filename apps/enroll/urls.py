'''
Author: shaojinxin shaojinxin@citorytech.com
Date: 2022-12-12 17:00:19
LastEditors: shaojinxin shaojinxin@citorytech.com
LastEditTime: 2022-12-20 15:18:12
FilePath: /metaweb_backend/apps/enroll/urls.py
Description: 

Copyright (c) 2022 by shaojinxin shaojinxin@citorytech.com, All Rights Reserved. 
'''
from django.urls import path

from .views import *

urlpatterns = [
    path('create/partner', create_partner.as_view(), name='create_partner'),
    path('create/product', create_product.as_view(), name='create_product'),
    path('create/group', create_group.as_view(), name='create_group'),
    path('search/partner', search_partner.as_view(), name='search_partner'),
    path('search/tag', search_tag.as_view(), name='search_tag'),
    path('search/group', search_group.as_view(), name='search_group'),
    path('list/occupation', list_occupation.as_view(), name='list_occupation'),
    path('list/category', list_category.as_view(), name='list_category'),
    path('list/fromtype', list_fromtype.as_view(), name='list_fromtype'),
    path('list/product', list_product.as_view(), name='list_product'),
    path('list/group', list_group.as_view(), name='list_group'),
    path('list/partner', list_partner.as_view(), name='list_partner'),
    path('get/content', get_content.as_view(), name='get_content'),
    path('update/partner', update_partner.as_view(), name='update_partner'),
    path('update/product', update_product.as_view(), name='update_product'),
    path('upload', upload_file.as_view(), name='upload_file'),
    #########################
    path('upload_project', upload_project, name='upload_project'),
    path('delete_project', delete_project, name='delete_project'),
    path('edit_project', edit_project, name='edit_project'),
    path('query_project_detail', query_project_detail, name='query_project_detail'),
    path('make_project_comment', make_project_comment, name='make_project_comment'),
    path('query_project_comment', query_project_comment, name='query_project_comment'),
    path('delete_project_comment', delete_project_comment, name='delete_project_comment'),
    path('query_project', query_project, name='query_project'),
    path('query_project_dot', query_project_dot, name='query_project_dot'),
    path('like_project', like_project, name='like_project'),
    path('unlike_project', unlike_project, name='unlike_project'),
    path('query_liked_projects', query_liked_projects, name='query_liked_projects'),
    path('search_for_projects', search_for_projects, name='search_for_projects'),
    path('search_for_users', search_for_users, name='search_for_users'),
    path('query_user_like_which', query_user_like_which, name='query_user_like_which'),
    path('query_all_project', query_all_project, name='query_all_project'),
    path('get_userinfo', get_userinfo, name='get_userinfo')
]