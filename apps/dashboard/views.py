'''
Author: shaojinxin shaojinxin@citorytech.com
Date: 2022-12-13 15:51:33
LastEditors: shaojinxin shaojinxin@citorytech.com
LastEditTime: 2023-04-17 17:22:56
FilePath: /metaweb_backend/apps/dashboard/views.py
Description: 

Copyright (c) 2022 by shaojinxin shaojinxin@citorytech.com, All Rights Reserved. 
'''
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.db.models import Q
from django.core import serializers
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.enroll.models import partner,group,product,occupation,category,content,social_like,social_view,social_share
import json,datetime,csv,decimal,os,re,hashlib
from pipe import select,where,groupby,sort
from project.myglobal import dictfetchall
from .color import pd_linear_gradient,RGB_to_hex,three_stop_gradient



class list_content(APIView):
    @swagger_auto_schema(operation_summary='作品清单', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        required=['fromtype'],
        properties={
            'fromtype': openapi.Schema(type=openapi.TYPE_NUMBER, description="大类"),
            'start_hex': openapi.Schema(type=openapi.TYPE_NUMBER, description="开始色"),
            'finish_hex': openapi.Schema(type=openapi.TYPE_NUMBER, description="结束色"),
            'mid_hex': openapi.Schema(type=openapi.TYPE_NUMBER, description="中间色"),
            'color_length': openapi.Schema(type=openapi.TYPE_NUMBER, description="颜色长度"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            fromtype = request.data['fromtype']
            with connection.cursor() as cursor:
                if fromtype == 1:# studio3
                    cursor.execute("""SELECT c.id as name,c.stage,c.date,q.point[1] as longitude,q.point[2] as latitude,category_id,color from metaweb.enroll_product_dif_regional q INNER JOIN metaweb.enroll_content c on q.id = c.product_id order by c.id;;""")
                    res = dictfetchall(cursor)
                elif fromtype == 2:# 科技追光
                    cursor.execute("""SELECT c.id as name,c.stage,c.date,q.point[1] as longitude,q.point[2] as latitude,category_id,color from metaweb.enroll_product_dif_regional_tech q INNER JOIN metaweb.enroll_content c on q.id = c.product_id and c.stage='end' order by c.id;""")
                    res = dictfetchall(cursor)
                elif fromtype == 3:# 地震
                    cursor.execute("""SELECT id,longitude,latitude,magnitude,location,date,depth_km,(round(percent_rank() over(ORDER BY magnitude)::numeric,2)*100)::int as coloridx from metaweb.earthquakes;""")
                    res = dictfetchall(cursor)
                    start_hex = request.data['start_hex']
                    finish_hex = request.data['finish_hex']
                    mid_hex = request.data['mid_hex']
                    color_length = int(request.data['color_length'])
                    result = three_stop_gradient(start_hex,finish_hex, mid_hex,color_length)
                    ans = []
                    for i in range(len(result)):
                        rgb = [result.r[i], result.g[i], result.b[i]]
                        ans.append(RGB_to_hex(rgb))
                    for i in res:
                        i['coloridx'] = int(i['coloridx']*(color_length-1)/100)
                        i['color'] = ans[i['coloridx']]
                        del i['coloridx']
                elif fromtype == 4:# 露营
                    start_hex = request.data['start_hex']
                    finish_hex = request.data['finish_hex']
                    mid_hex = request.data['mid_hex']
                    color_length = int(request.data['color_length'])
                    cursor.execute(f"""SELECT id,name,date(navi_update_time),addr,city_name||' '||area_name as area,image,phone,longitude,latitude,(cume_dist() over( order by navi_update_time)*100)::int as coloridx from metaweb.camping;""")
                    res = dictfetchall(cursor)
                    result = three_stop_gradient(start_hex,finish_hex, mid_hex,color_length)
                    ans = []
                    for i in range(len(result)):
                        rgb = [result.r[i], result.g[i], result.b[i]]
                        ans.append(RGB_to_hex(rgb))
                    for i in res:
                        i['coloridx'] = int(i['coloridx']*(color_length-1)/100)
                        i['color'] = ans[i['coloridx']]
                        del i['coloridx']
                print(res)
                return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class get_content_detail(APIView):
    @swagger_auto_schema(operation_summary='获取作品详情', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        required=['id'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER, description="ID")
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            id = request.data['id']
            res= list(content.objects.filter(id=id).values('product__fromtype__name','product__name','product__group__name','product__regional','product__point','product__category__name','product__tags','product__description','stage','date','album','images','video','model','slide','pdf'))
            if len(res)>0:
                return JsonResponse(dict(data=res[0], status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class content_social_like(APIView):
    @swagger_auto_schema(operation_summary='作品点赞', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        required=['content_id', 'user_id'],
        properties={
            'content_id': openapi.Schema(type=openapi.TYPE_NUMBER, description="作品ID"),
            'user_id': openapi.Schema(type=openapi.TYPE_STRING, description="用户ID"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            content_id = request.data['content_id']
            user_id = request.data['user_id']
            _content = content.objects.filter(id=content_id)
            product_name = _content.values('product__name').first()['product__name']
            s = social_like.objects.filter(content=_content[0], user=user_id)
            if not s.exists():
                social_like.objects.create(content=_content[0], user=user_id)
                return JsonResponse(dict(data=f'用户『{user_id}』 为作品『{product_name}』点赞成功', status=True, code=200))
            else:
                return JsonResponse(dict(data=f'用户『{user_id}』 已为作品『{product_name}』点过赞', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))


class content_social_view(APIView):
    @swagger_auto_schema(operation_summary='作品观看', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        required=['content_id', 'user_id'],
        properties={
            'content_id': openapi.Schema(type=openapi.TYPE_NUMBER, description="作品ID"),
            'user_id': openapi.Schema(type=openapi.TYPE_STRING, description="用户ID"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            content_id = request.data['content_id']
            user_id = request.data['user_id']
            _content = content.objects.filter(id=content_id)
            product_name = _content.values('product__name').first()['product__name']
            social_view.objects.create(content=_content.first(), user=user_id)
            return JsonResponse(dict(data=f'用户『{user_id}』 观看作品『{product_name}』', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class content_social_share(APIView):
    @swagger_auto_schema(operation_summary='作品分享', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        required=['content_id', 'user_id'],
        properties={
            'content_id': openapi.Schema(type=openapi.TYPE_NUMBER, description="作品ID"),
            'user_id': openapi.Schema(type=openapi.TYPE_STRING, description="用户ID"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            content_id = request.data['content_id']
            user_id = request.data['user_id']
            _content = content.objects.filter(id=content_id)
            product_name = _content.values('product__name').first()['product__name']
            social_share.objects.create(content=_content.first(), user=user_id)
            return JsonResponse(dict(data=f'用户『{user_id}』 分享作品『{product_name}』', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))



