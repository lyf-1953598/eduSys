'''
Descripttion: 
version: 
Author: shaojinxin
Date: 2021-08-12 18:15:42
LastEditors: shaojinxin shaojinxin@citorytech.com
LastEditTime: 2022-12-12 19:08:03
'''
from django.core.cache import cache
from django_redis import get_redis_connection
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import *

import json,datetime,time,logging,os
from logging import handlers
from functools import wraps
# from jose import jwt, JWTError, ExpiredSignatureError
'''
Descripttion: token 验证
TODO: 
param {*}
return {*}
'''
TEST_TOKEN_LIST = ['ykr47uA19fWxJllJV75doP58mCE5knQ7ulguiuDzmCeqfUDQZuQMOLtNCc8WmJ48']
def login_required():
    def decorator(viewfunc):
        @wraps(viewfunc)
        def wrapper(self, request, *args, **kwargs):
            # token = request.META.get('HTTP_AUTHORIZATION')
            token= request.META.get('HTTP_TOKEN')
            if not token:
                return JsonResponse(dict(meaasge='request header 缺少 Bearer Token', status=False, code=401))
            else:
                token = token.replace('Bearer ', '')
                try:
                    if token not in TEST_TOKEN_LIST:
                        return JsonResponse(dict(message='bad token!', status=False, code=401))
                except Exception as r:
                    return JsonResponse(dict(message=r, status=False, code=403))
            return viewfunc(self, request, *args, **kwargs)
        return wrapper
    return decorator