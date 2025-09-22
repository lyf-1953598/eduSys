'''
Author: shaojinxin shaojinxin@citorytech.com
Date: 2022-12-12 19:07:39
LastEditors: shaojinxin shaojinxin@citorytech.com
LastEditTime: 2023-04-24 16:47:51
FilePath: /metopia/backend/apps/enroll/views.py
Description: 

Copyright (c) 2022 by shaojinxin shaojinxin@citorytech.com, All Rights Reserved. 
'''
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.db.models import Q
from django.core import serializers
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .decorator import *
from .models import *
import json,datetime,csv,decimal,os,re,hashlib
from pipe import select,where,groupby,sort
# from project.myglobal import cosclient,dictfetchall,_logging
from project.myglobal import _logging
from django.conf import settings
# from qcloud_cos.cos_exception import CosClientError, CosServiceError
import exifread
import base64
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.system.models import user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from openai import OpenAI
import re

logger = _logging(filename='./logs/enroll.log')
STATIC_URL = 'static/upload/'

class create_partner(APIView):
    @swagger_auto_schema(operation_summary='新建作者', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'occupation'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="作者姓名"),
            'gender': openapi.Schema(type=openapi.TYPE_STRING, description="作者性别"),
            'regional': openapi.Schema(type=openapi.TYPE_STRING, description="出生地"),
            'point':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_NUMBER),description="出生地经纬度"),
            'avatar':openapi.Schema(type=openapi.TYPE_STRING, description="作者头像地址"),
            'signature':openapi.Schema(type=openapi.TYPE_STRING, description="个性签名"),
            'occupation':openapi.Schema(type=openapi.TYPE_NUMBER, description="职业"),
            'email':openapi.Schema(type=openapi.TYPE_STRING, description="邮箱"),
            'phone':openapi.Schema(type=openapi.TYPE_STRING, description="手机"),
        },
    ))
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        gender = request.data['gender']
        regional = request.data['regional']
        point = request.data['point']
        avatar = request.data['avatar'] if 'avatar' in request.data.keys() else None
        signature = request.data['signature'] if 'signature' in request.data.keys() else None
        email = request.data['email'] if 'email' in request.data.keys() else None
        phone = request.data['phone'] if 'phone' in request.data.keys() else None
        _occupation = occupation.objects.get(id=int(request.data['occupation'])) if 'occupation' in request.data.keys() else None
        try:
            partner.objects.create(name=name, email=email,phone=phone,gender=gender,regional=regional,point=point, avatar=avatar, signature=signature,occupation= _occupation )
            return JsonResponse(dict(data=f'新建作者『{name}』成功', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class update_partner(APIView):
    @swagger_auto_schema(operation_summary='更新作者信息', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id'],
        properties={
            'id':openapi.Schema(type=openapi.TYPE_NUMBER, description="作者ID"),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="作者姓名"),
            'gender': openapi.Schema(type=openapi.TYPE_STRING, description="作者性别"),
            'regional': openapi.Schema(type=openapi.TYPE_STRING, description="出生地"),
            'point':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_NUMBER),description="出生地经纬度"),
            'avatar':openapi.Schema(type=openapi.TYPE_STRING, description="作者头像地址"),
            'signature':openapi.Schema(type=openapi.TYPE_STRING, description="个性签名"),
            'occupation__id':openapi.Schema(type=openapi.TYPE_NUMBER, description="职业"),
            'email':openapi.Schema(type=openapi.TYPE_STRING, description="邮箱"),
            'phone':openapi.Schema(type=openapi.TYPE_STRING, description="手机"),
        },
    ))
    def post(self, request, *args, **kwargs):
        id = request.data['id'] 
        name = request.data['name'] if 'name' in request.data.keys() else None
        gender = request.data['gender'] if 'gender' in request.data.keys() else None
        regional = request.data['regional'] if 'regional' in request.data.keys() else None
        point = request.data['point'] if 'point' in request.data.keys() else None
        avatar = request.data['avatar'] if 'avatar' in request.data.keys() else None
        signature = request.data['signature'] if 'signature' in request.data.keys() else None
        email = request.data['email'] if 'email' in request.data.keys() else None
        phone = request.data['phone'] if 'phone' in request.data.keys() else None
        _occupation = occupation.objects.get(id=int(request.data['occupation__id'])) if 'occupation__id' in request.data.keys() else None
        try:
            _partner = partner.objects.filter(id=int(id))
            _partner.update(name=name, email=email,phone=phone,gender=gender,regional=regional,point=point, avatar=avatar, signature=signature,occupation= _occupation )
            return JsonResponse(dict(data=f'更新作者『{name}』成功', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class create_group(APIView):
    @swagger_auto_schema(operation_summary='新建小组', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'leader','member'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="小组名称"),
            'leader': openapi.Schema(type=openapi.TYPE_STRING, description="组长"),
            'member': openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description="组员"),
        },
    ))
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        leader = request.data['leader']
        member = request.data['member']
        # logger.info(partner.objects.filter(name=name))
        try:
            group.objects.create(name=name, leader=partner.objects.filter(name=leader)[0],member=member)
            return JsonResponse(dict(data='新建小组成功', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class create_product(APIView):
    @swagger_auto_schema(operation_summary='注册作品', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['product_form', 'content_mid_form','content_end_form'],
        properties={
            'group_form': openapi.Schema(type=openapi.TYPE_OBJECT, description="小组表单"),
            'product_form_data': openapi.Schema(type=openapi.TYPE_OBJECT, description="作品表单"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            product_form = request.data['product_form_data']
            if 'group_form' in request.data.keys():
                group_form = request.data['group_form']
                _leader = partner.objects.filter(name=group_form['leader'])
                if not _leader.exists():
                    return JsonResponse(dict(message='组长不存在，请创建作者并提交作者信息后重新提交项目！', status=False, code=200))
                _leader = _leader[0]
                _group = group.objects.filter(name=group_form['name'],leader=_leader)
                if not _group.exists():
                    _group = group(name=group_form['name'], leader=partner.objects.filter(name=group_form['leader'])[0],member=group_form['member'])
                    _group.save()
                    logger.info(f"注册小组成功:{group_form['name']}")
                else:
                    _group = _group[0]
                    logger.info(f"小组已存在:{group_form['name']}")
            else:
                _group = group.objects.filter(name=product_form['group'])
                if not _group.exists():
                    return JsonResponse(dict(message='小组信息错误，请重新选择或创建新的小组。', status=False, code=200))
                else:
                    _group = _group[0]
            _category = category.objects.filter(id=product_form['category'])[0]
            product_name = product_form['name']
            _fromtype = product_form['fromtype'] if 'fromtype' in product_form.keys() else 1
            _product = product.objects.filter(fromtype__id=_fromtype,name=product_name,group=_group)
            if not _product.exists():
                _product = product(fromtype=fromtype.objects.get(id=_fromtype),name=product_name,group=_group,regional=product_form['regional'],point=product_form['point'],category=_category,tags=product_form['tags'],description=product_form['description'])
                _product.save()
                logger.info(f"项目保存成功:{product_name}")
            else:
                _product.update(name=product_name,group=_group,regional=product_form['regional'],point=product_form['point'],category=_category,tags=product_form['tags'],description=product_form['description'])
                logger.info(f"项目更新成功:{product_name}")
                _product = _product[0]
            cmid = content.objects.filter(product=_product,stage='mid')
            if not cmid.exists():
                content.objects.create(product=_product,stage='mid',date=product_form['mid_date'],album=product_form['mid_album'],images=product_form['mid_images'])
                logger.info(f"中期保存成功:{product_name}")
            else:
                cmid.update(product=_product,stage='mid',date=product_form['mid_date'],album=product_form['mid_album'],images=product_form['mid_images'])
            cend = content.objects.filter(product=_product,stage='end')
            if not cend.exists():
                content.objects.create(product=_product,stage='end',date=product_form['end_date'],album=product_form['end_album'],images=product_form['end_images'],video=product_form['end_video'],model=product_form['end_model'],slide=product_form['end_slide'],pdf=product_form['end_pdf'])
                logger.info(f"终期保存成功:{product_name}")
            else:
                cend.update(product=_product,stage='end',date=product_form['end_date'],album=product_form['end_album'],images=product_form['end_images'],video=product_form['end_video'],model=product_form['end_model'],slide=product_form['end_slide'],pdf=product_form['end_pdf'])
            return JsonResponse(dict(data=f'新建作品『{product_name}』成功', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))


class update_product(APIView):
    @swagger_auto_schema(operation_summary='更新作品基础信息', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER, description="项目ID"),
            'name':openapi.Schema(type=openapi.TYPE_STRING, description="项目名称"),
            'regional':openapi.Schema(type=openapi.TYPE_STRING, description="位置"),
            'point':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_NUMBER), description="经纬度"),
            'description':openapi.Schema(type=openapi.TYPE_STRING, description="项目描述"),
            'tags':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description="标签"),
            'category__id': openapi.Schema(type=openapi.TYPE_STRING, description="研究方向"),
            'fromtype__id': openapi.Schema(type=openapi.TYPE_STRING, description="大类"),
            'group__id': openapi.Schema(type=openapi.TYPE_STRING, description="小组ID"),
            'group__name': openapi.Schema(type=openapi.TYPE_STRING, description="小组名称"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            id = request.data['id'] 
            name = request.data['name'] if 'name' in request.data.keys() else None
            regional = request.data['regional'] if 'regional' in request.data.keys() else None
            point = request.data['point'] if 'point' in request.data.keys() else None
            description = request.data['description'] if 'description' in request.data.keys() else None
            tags = request.data['tags'] if 'tags' in request.data.keys() else None
            category__id = request.data['category__id'] if 'category__id' in request.data.keys() else None
            fromtype__id = request.data['fromtype__id'] if 'fromtype__id' in request.data.keys() else None
            group__id = request.data['group__id'] if 'group__id' in request.data.keys() else None
            group__name = request.data['group__name'] if 'group__name' in request.data.keys() else None
            _group =group.objects.get(id=group__id)
            if group__name!=_group.name:
                _group.name = group__name
                _group.save()
            _category = category.objects.get(id=category__id)
            _fromtype = fromtype.objects.get(id=fromtype__id)
            _product = product.objects.filter(id=id)
            _product.update(fromtype=_fromtype,name=name,group=_group,regional=regional,point=point,category=_category,tags=tags,description=description)
            return JsonResponse(dict(data=f'更新作品『{name}』成功', status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))
class search_partner(APIView):
    @swagger_auto_schema(operation_summary='查找作者', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="作者姓名"),
            'gender': openapi.Schema(type=openapi.TYPE_STRING, description="作者性别"),
            'regional': openapi.Schema(type=openapi.TYPE_STRING, description="出生地"),
            'signature':openapi.Schema(type=openapi.TYPE_STRING, description="个性签名"),
            'occupation':openapi.Schema(type=openapi.TYPE_STRING, description="职业")
        },
    ))
    def post(self, request, *args, **kwargs):
        
        if 'name' in request.data.keys():
            if request.data['name'] == "":
                return JsonResponse(dict(message='empty name', status=False, code=200))
            p = partner.objects.filter(name__icontains=request.data['name'])
        if 'gender' in request.data.keys():
            p = partner.objects.filter(gender=request.data['gender'])
        if 'regional' in request.data.keys():
            p = partner.objects.filter(regional__icontains=request.data['regional'])
        if 'signature' in request.data.keys():
            p = partner.objects.filter(signature__icontains=request.data['signature'])
        if 'occupation' in request.data.keys():
            p = partner.objects.filter(occupation=request.data['occupation'])
        try:
            res = list(p.values())
            return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class search_tag(APIView):
    @swagger_auto_schema(operation_summary='搜索作品标签', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="标签")
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            res = list(tags.objects.filter(name__icontains=request.data['name']).values())
            return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class search_group(APIView):
    @swagger_auto_schema(operation_summary='搜索小组', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="小组")
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            res = list(group.objects.filter(name__icontains=request.data['name']).values())
            res = list(res | select(lambda x:{"id":x["id"], "name":x["name"],"leader":partner.objects.get(id=x["leader_id"]).name}))
            return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))
        
class list_occupation(APIView):
    @swagger_auto_schema(operation_summary='枚举职业', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT
    ))
    def post(self, request, *args, **kwargs):
        try:
            res = list(occupation.objects.all().values())
            return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class list_category(APIView):
    @swagger_auto_schema(operation_summary='枚举作品类别', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT
    ))
    def post(self, request, *args, **kwargs):
        try:
            res = list(category.objects.all().values())
            return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))


class list_fromtype(APIView):
    @swagger_auto_schema(operation_summary='枚举作品来源', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT
    ))
    def post(self, request, *args, **kwargs):
        try:
            res = list(fromtype.objects.all().values())
            return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class list_product(APIView):
    @swagger_auto_schema(operation_summary='作品清单', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            'pagenum': openapi.Schema(type=openapi.TYPE_NUMBER, description="页码"),
            'pagelength': openapi.Schema(type=openapi.TYPE_NUMBER, description="每页长度"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            if 'pagenum' in request.data.keys() and 'pagelength' in request.data.keys():
                startRow = (request.data['pagenum']-1)*request.data['pagelength']
                endRow = request.data['pagenum'] * request.data['pagelength']
                res = list(product.objects.all().order_by('pk')[startRow:endRow].values('id','fromtype__id','fromtype__name','name','group__id','group__name','regional','point','category__id','category__name','tags','description'))
            else:
                res = list(product.objects.all().order_by('pk').values('id','fromtype__id','fromtype__name','name','group__id','group__name','regional','point','category__id','category__name','tags','description'))
            count = product.objects.all().count()
            return JsonResponse(dict(data={"data":res,"total":count}, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class list_group(APIView):
    @swagger_auto_schema(operation_summary='小组清单', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            'pagenum': openapi.Schema(type=openapi.TYPE_NUMBER, description="页码"),
            'pagelength': openapi.Schema(type=openapi.TYPE_NUMBER, description="每页长度"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            if 'pagenum' in request.data.keys() and 'pagelength' in request.data.keys():
                startRow = (request.data['pagenum']-1)*request.data['pagelength']
                endRow = request.data['pagenum'] * request.data['pagelength']
                res = list(group.objects.all().order_by('pk')[startRow:endRow].values('id','name','leader__id','leader__name','member'))
            else:
                res = list(group.objects.all().order_by('pk').values('id','name','leader__id','leader__name','member'))
            count = group.objects.all().count()
            return JsonResponse(dict(data={"data":res,"total":count}, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class list_partner(APIView):
    @swagger_auto_schema(operation_summary='作者清单', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            'pagenum': openapi.Schema(type=openapi.TYPE_NUMBER, description="页码"),
            'pagelength': openapi.Schema(type=openapi.TYPE_NUMBER, description="每页长度"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            if 'pagenum' in request.data.keys() and 'pagelength' in request.data.keys():
                startRow = (request.data['pagenum']-1)*request.data['pagelength']
                endRow = request.data['pagenum'] * request.data['pagelength']
                res = list(partner.objects.all().order_by('pk')[startRow:endRow].values('id','name','gender','regional','point','avatar','signature','occupation__id','occupation__name','email','phone'))
            else:
                res = list(partner.objects.all().order_by('pk').values('id','name','gender','regional','point','avatar','signature','occupation__id','occupation__name','email','phone'))
            count = partner.objects.all().count()
            return JsonResponse(dict(data={"data":res,"total":count}, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))
        
class get_content(APIView):
    @swagger_auto_schema(operation_summary='获取作品内容', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER, description="项目id"),
        },
    ))
    def post(self, request, *args, **kwargs):
        try:
            bac = list(content.objects.filter(product__id=request.data['id']).values('product__name','stage','date','album','images','video','model','slide','pdf'))
            res = {}
            for i in bac:
                res[i['stage']]={}
                for j in i:
                    if i[j]!=None and i[j]!=[]:
                        res[i['stage']][j]=i[j]
            return JsonResponse(dict(data=res, status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=200))

class upload_file(APIView):
    @swagger_auto_schema(operation_summary='上传文件',request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['file'],
            properties={
                'extra':openapi.Schema(type=openapi.TYPE_STRING, description="额外参数"),                
                'file': openapi.Schema(type=openapi.TYPE_FILE,description="上传文件"),
            },
        ))
    def post(self, request,*args, **kwargs):
        try:
            myFile = request.FILES.get("file", None)
            # md5重命名
            md5obj = hashlib.md5()
            md5obj.update(myFile.read())
            hash = md5obj.hexdigest()
            formatname =str(hash)+'_'+myFile.name
            # 保存位置
            inner_path = os.path.join(settings.LOCAL_DIR,STATIC_URL,formatname)
            destination = open(inner_path,'wb+')    # 打开特定的文件进行二进制的写操作  
            for chunk in myFile.chunks():      # 分块写入文件  
                destination.write(chunk)  
            destination.close()
            # 使用高级接口断点续传，失败重试时不会上传已成功的分块(这里重试10次)
            # for i in range(0, 10):
            #     try:
            #         response = cosclient.upload_file(
            #         Bucket='metaweb-1254980686',
            #         Key=formatname,
            #         LocalFilePath=inner_path)
            #         break
            #     except CosClientError or CosServiceError as e:
            #         print(e)
            extra = request.data['extra'] if 'extra' in request.data.keys() else None
            res = {"name":formatname,"extra":extra,"url":f'https://metaweb-1254980686.cos.ap-shanghai.myqcloud.com/{formatname}'}
            if extra == 'getLocation':
                coors = get_location(myFile)
                res['coors'] = coors
                del res['extra']
            return JsonResponse(dict(data=res,status=True, code=200))
        except Exception as r:
            return JsonResponse(dict(message=str(r), status=False, code=400))

def convert2latlon(x):    
    # 处理经纬度 将其转化为 xx.xxxxxx格式
    x_last = eval(str(x[-1]))
    new_x = x[0].num + x[1].num / 60 + x_last / 3600
    return str(new_x)
# bytes 转 base64
def bytes_to_base64(image_bytes):    
    image_base4 = base64.b64encode(image_bytes).decode('utf8')
    return image_base4

def get_location(myFile):
    # 获取图片信息
    # f = open(path,"rb")   # 读取图片为二进制格式
    tags = exifread.process_file(myFile)
    # 图片纬度
    lat = tags.get('GPS GPSLatitude', '0').values if 'GPS GPSLatitude' in tags.keys() else None
    lat = convert2latlon(lat) if lat is not None else None
    # 图片经度
    lon = tags.get('GPS GPSLongitude', '0').values if 'GPS GPSLongitude' in tags.keys() else None
    lon = convert2latlon(lon) if lon is not None else None
    # 获取日期，时间
    date =  tags.get('EXIF DateTimeDigitized').values if 'EXIF DateTimeDigitized' in tags.keys() else None
    thumbnail = bytes_to_base64(tags.get('JPEGThumbnail')) if 'JPEGThumbnail' in tags.keys() else None
    return{"lon":lon,"lat":lat,"date":date,"thumbnail":thumbnail}


@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('userid', openapi.IN_QUERY, description="ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('name', openapi.IN_QUERY, description="名字", type=openapi.TYPE_STRING),
        openapi.Parameter('location', openapi.IN_QUERY, description="位置", type=openapi.TYPE_STRING),
        openapi.Parameter('longitude', openapi.IN_QUERY, description="经度", type=openapi.TYPE_NUMBER),
        openapi.Parameter('latitude', openapi.IN_QUERY, description="纬度", type=openapi.TYPE_NUMBER),
        openapi.Parameter('category', openapi.IN_QUERY, description="种类", type=openapi.TYPE_STRING),
        openapi.Parameter('keyword', openapi.IN_QUERY, description="关键词", type=openapi.TYPE_STRING),
        openapi.Parameter('description', openapi.IN_QUERY, description="详情描述", type=openapi.TYPE_STRING),
        openapi.Parameter('image', openapi.IN_QUERY, description="图片", type=openapi.TYPE_FILE),
        openapi.Parameter('video', openapi.IN_QUERY, description="视频", type=openapi.TYPE_FILE),
        openapi.Parameter('file', openapi.IN_QUERY, description="文件", type=openapi.TYPE_FILE),
    ]
)
@api_view(['POST'])
def upload_project(request):
    response = {}

    # 检测图片是否上传
    if 'image' not in request.FILES:
        response['status'] = 'Fail'
        response['msg'] = "Image is required."
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    userid = request.data['userid']
    name = request.data['name']
    location = request.data['location']
    longitude = request.data['longitude']
    latitude = request.data['latitude']
    category = request.data['category']
    keyword = request.data['keyword']
    description = request.data['description']

    image = request.FILES['image']  # 图片是必需的
    video = request.FILES.get('video')  # 视频是可选的
    file = request.FILES.get('file')  # 文件是可选的

    # 检查字段是否为空
    if not all([userid, name, location, longitude, latitude, category, keyword, description]) or not image:
        response['status'] = 'Fail'
        response['msg'] = 'Invalid data provided'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 检查能否找到该用户
    try:
        current_user = user.objects.get(id=userid)
    except user.DoesNotExist:
        response = {
            'status': 'Fail',
            'msg': 'User with the given ID does not exist'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        response = {
            'status': 'Fail',
            'msg': 'Invalid data provided'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 检测经纬度范围
    if float(longitude) < -180 or float(longitude) > 180 or float(latitude) < -90 or float(latitude) > 90:
        response = {
            'status': 'Fail',
            'msg': 'Invalid latitude or longitude range.'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 定义文件存储路径
    media_directory = 'D:\Github_code\Metaweb2024\metapia_frontend\public\media'  # 需改成自己本地的public路径
    image_directory = os.path.join(media_directory, 'image')
    video_directory = os.path.join(media_directory, 'video')
    file_directory = os.path.join(media_directory, 'file')

    for directory in [image_directory, video_directory, file_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # 生成图片文件路径
    unique_image_id = uuid.uuid4()
    image_extension = os.path.splitext(image.name)[1]  # 获取图片扩展名
    image_filename = f"{unique_image_id}{image_extension}"  # 生成唯一图片文件名
    image_path = os.path.join(image_directory, image_filename)
    # 保存图片文件到指定路径
    with open(image_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    video_filename = None
    # 如果提供了视频，则保存视频
    if video:
        unique_video_id = uuid.uuid4()
        video_extension = os.path.splitext(video.name)[1]
        video_filename = f"{unique_video_id}_video{video_extension}"
        video_path = os.path.join(video_directory, video_filename)
        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)
    file_filename = None
    # 如果提供了文件，则保存文件
    if file:
        unique_file_id = uuid.uuid4()
        file_extension = os.path.splitext(file.name)[1]
        file_filename = f"{unique_file_id}_file{file_extension}"
        file_path = os.path.join(file_directory, file_filename)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    try:
        new_project = Project(
            name=name,
            location=location,
            longitude=longitude,
            latitude=latitude,
            category=category,
            keyword=keyword,
            description=description,
            image=image_filename,  # 图片文件路径
            video=video_filename,
            file=file_filename
        )
        new_project.save()

        upload_record = UploadProject(
            user=current_user,
            project=new_project
        )
        upload_record.save()

        response['status'] = 'OK'
        return Response(response)
    except Exception as e:
        response['status'] = 'Fail'
        response['msg'] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_project(request):
    response = {}

    # # 检查字段是否存在
    # if 'project_id' not in request.data:
    #     response['status'] = 'Fail'
    #     response['msg'] = 'Missing required fields'
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    project_id = request.data['project_id']
    # 检查字段是否为空
    if not project_id:
        response['status'] = 'Fail'
        response['msg'] = 'Invalid data provided'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 检查能否找到该项目
    try:
        project_to_delete = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        response = {
            'status': 'Fail',
            'msg': 'Project with the given ID does not exist'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        # 如果传递的项目ID无效，如非数字字符串
        response = {
            'status': 'Fail',
            'msg': 'Invalid data provided'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    project_to_delete.delete()
    return Response({"message": "项目删除成功"}, status=200)

@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('project_id', openapi.IN_QUERY, description="ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('name', openapi.IN_QUERY, description="名字", type=openapi.TYPE_STRING),
        openapi.Parameter('location', openapi.IN_QUERY, description="位置", type=openapi.TYPE_STRING),
        openapi.Parameter('longitude', openapi.IN_QUERY, description="经度", type=openapi.TYPE_NUMBER),
        openapi.Parameter('latitude', openapi.IN_QUERY, description="纬度", type=openapi.TYPE_NUMBER),
        openapi.Parameter('category', openapi.IN_QUERY, description="种类", type=openapi.TYPE_STRING),
        openapi.Parameter('keyword', openapi.IN_QUERY, description="关键词", type=openapi.TYPE_STRING),
        openapi.Parameter('description', openapi.IN_QUERY, description="详情描述", type=openapi.TYPE_STRING),
        openapi.Parameter('image', openapi.IN_QUERY, description="图片", type=openapi.TYPE_FILE),
        openapi.Parameter('video', openapi.IN_QUERY, description="视频", type=openapi.TYPE_FILE),
        openapi.Parameter('file', openapi.IN_QUERY, description="文件", type=openapi.TYPE_FILE),
    ]
)
@api_view(['POST'])
def edit_project(request):
    response = {}

    # 检测文件是否上传
    # if 'image' not in request.FILES:
    #     response['status'] = 'Fail'
    #     response['error'] = "Image isn't provided"
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    project_id = request.data['project_id']
    name = request.data['name']
    location = request.data['location']
    longitude = request.data['longitude']
    latitude = request.data['latitude']
    category = request.data['category']
    keyword = request.data['keyword']
    description = request.data['description']
    image = request.FILES['image']
    video = request.FILES.get('video')
    file = request.FILES.get('file')

    # 检查字段是否为空
    if not all([project_id, name, location, longitude, latitude, category, keyword, description]) or not image:
        response['status'] = 'Fail'
        response['error'] = 'Invalid data provided'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 检查能否找到该项目
    try:
        project_to_update = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        response = {
            'status': 'Fail',
            'msg': 'Project with the given ID does not exist'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        # 如果传递的项目ID无效，如非数字字符串
        response = {
            'status': 'Fail',
            'msg': 'Invalid data provided'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 检测经纬度范围
    if float(longitude) < -180 or float(longitude) > 180 or float(latitude) < -90 or float(latitude) > 90:
        response = {
            'status': 'Fail',
            'msg': 'Invalid latitude or longitude range.'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # 文件存储路径
    media_directory = 'D:\Github_code\Metaweb2024\metapia_frontend\public\media'  # 需改成自己本地的public路径
    image_directory = os.path.join(media_directory, 'image')
    video_directory = os.path.join(media_directory, 'video')
    file_directory = os.path.join(media_directory, 'file')

    # 生成图片路径
    unique_image_id = uuid.uuid4()
    file_extension = os.path.splitext(image.name)[1]  # 获取文件扩展名
    image_filename = f"{unique_image_id}{file_extension}"  # 生成唯一文件名
    image_path = os.path.join(image_directory, image_filename)

    # 保存文图片到指定路径
    with open(image_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    # 移除之前的 image
    os.remove(os.path.join(image_directory, project_to_update.image))

    # 修改了 video
    if video:
        video_filename = None
        unique_video_id = uuid.uuid4()
        video_extension = os.path.splitext(video.name)[1]
        video_filename = f"{unique_video_id}_video{video_extension}"
        video_path = os.path.join(video_directory, video_filename)

        # 保存新 video
        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)

        # 删除旧的 video 文件
        if project_to_update.video:
            old_video_path = os.path.join(video_directory, project_to_update.video)
            if os.path.exists(old_video_path):
                os.remove(old_video_path)

        project_to_update.video = video_filename

    # 修改了 file
    if file:
        file_filename = None
        unique_file_id = uuid.uuid4()
        file_extension = os.path.splitext(file.name)[1]
        file_filename = f"{unique_file_id}_file{file_extension}"
        file_path = os.path.join(file_directory, file_filename)

        # 保存新 file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 删除旧的 file 文件
        if project_to_update.file:
            old_file_path = os.path.join(file_directory, project_to_update.file)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        project_to_update.file = file_filename

    try:
        project_to_update.image = image_filename
        project_to_update.name = name
        project_to_update.location = location
        project_to_update.longitude = longitude
        project_to_update.latitude = latitude
        project_to_update.category = category
        project_to_update.keyword = keyword
        project_to_update.description = description
        project_to_update.save()
        return Response({"msg": "项目更新成功"}, status=200)
    except Exception as e:
        response['status'] = 'Fail'
        response['msg'] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('userid', openapi.IN_QUERY, description="ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('category', openapi.IN_QUERY, description="类型", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="页号", type=openapi.TYPE_INTEGER),
        openapi.Parameter('per_page', openapi.IN_QUERY, description="每页数量", type=openapi.TYPE_INTEGER)
    ]
)
#查询项目浏览
@api_view(['GET'])
def query_project(request):
    response = {}

    # 获取查询参数
    userid = request.GET.get('userid')
    project_category = request.GET.get('category')
    page = request.GET.get('page', 1)  # 默认页码为1
    per_page = 10  # 每页显示10个项目

    # 查询项目列表
    projects = Project.objects.all()

    # 根据用户ID查询作者的所有作品
    if userid:
        if not userid.isdigit():
            return Response({"error": "无效的用户ID"}, status=status.HTTP_400_BAD_REQUEST)
        project_ids = UploadProject.objects.filter(user_id=userid).values_list('project_id', flat=True)
        projects = Project.objects.filter(id__in=project_ids)

    # 根据类型查询
    #if project_category.strip() == "":
        #return Response({"error": "项目类别为空"}, status=status.HTTP_400_BAD_REQUEST)

    # 根据类型查询
    if project_category and project_category.strip():
        projects = Project.objects.filter(category=project_category)

    if not projects.exists():
        return Response({"error": "未找到符合条件的项目"}, status=status.HTTP_404_NOT_FOUND)

    paginator = Paginator(projects, per_page)

    # 检查page是否在合法范围内
    if page < 1 or page > paginator.num_pages:
        return Response({"error": f"页号不在合法范围内, 应在1到{paginator.num_pages}之间"},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        paginated_projects = paginator.page(page)
    except PageNotAnInteger:
        return Response({"error": "页号错误"}, status=status.HTTP_400_BAD_REQUEST)
    except EmptyPage:
        paginated_projects = paginator.page(paginator.num_pages)

    projects_data = []
    for project in paginated_projects:
        projects_data.append({
            'id': project.id,
            'name': project.name,
            'likes': project.likes,
            'image': project.image,  # 上传的图片作为封面
            'location': project.location,
            'longitude': project.longitude,
            'latitude': project.latitude,
            'description': project.description
        })

    response['projects'] = projects_data
    response['total_count'] = projects.count()
    response['total_pages'] = paginator.num_pages

    return Response(response, status=200)

# 方便在地球上展示点
@swagger_auto_schema(
    method='get',
    manual_parameters=[
    ]
)
@api_view(['GET'])
def query_project_dot(request):
    response = []
    project_ids = UploadProject.objects.values_list('project_id', flat=True)
    projects = Project.objects.filter(id__in=project_ids)
    # 暂时没有验证发布人是否合法
    if projects.exists():
        for project in projects:
            response.append({
                'id': project.id,
                'longitude': project.longitude,
                'latitude': project.latitude,
                'size': project.likes
            })
    else:
        return Response({'status': 'Fail', 'msg': '项目为空'}, status=404)
    return Response(response)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('project_id', openapi.IN_QUERY, description="项目id", type=openapi.TYPE_INTEGER),
        openapi.Parameter('userid', openapi.IN_QUERY, description="用户id", type=openapi.TYPE_INTEGER),
    ]
)
@api_view(['GET'])
def query_project_detail(request):
    response = {}
    project_id = request.GET.get('project_id')
    userid = request.GET.get('userid')

    if not project_id:
        return Response({"error": "缺少项目ID参数"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 获取项目详情
        project_detail = Project.objects.get(id=project_id)

        # 构建响应数据
        response['project'] = {
            'name': project_detail.name,
            'location': project_detail.location,
            'longitude': project_detail.longitude,
            'latitude': project_detail.latitude,
            'category': project_detail.category,
            'description': project_detail.description,
            'likes': project_detail.likes,
            'image': project_detail.image,
        }
        if project_detail.video:
            response['project']['file'] = project_detail.video
        if project_detail.file:
            response['project']['file'] = project_detail.file

        # 获取项目的作者信息
        upload_record = UploadProject.objects.filter(project=project_detail).first()
        if upload_record:
            response['project']['author'] = upload_record.user.name

        # 判断当前用户是否对该项目点过赞
        if userid:
            try:
                has_liked = project_like.objects.filter(user_id=userid, project=project_detail).exists()
                response['project']['has_liked'] = has_liked
            except user.DoesNotExist:
                response['project']['has_liked'] = False
        else:
            response['project']['has_liked'] = False

        return Response(response, status=status.HTTP_200_OK)

    except Project.DoesNotExist:
        # 项目不存在
        return Response({"error": "项目不存在"}, status=status.HTTP_404_NOT_FOUND)

    except ValueError:
        # 如果传递的项目ID无效，如非数字字符串
        return Response({"error": "无效的项目ID"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # 捕获其他未知错误
        return Response({"error": f"服务器内部错误: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 评论项目
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userid': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户ID'),
            'projectid': openapi.Schema(type=openapi.TYPE_INTEGER, description='项目ID'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='评论内容')
        }
    )
)
@api_view(['POST'])
def make_project_comment(request):
    response = {}
    userid = request.data['userid']
    projectid = request.data['projectid']
    content = request.data['content']

    if content and userid and projectid:
        # 查找用户及项目是否存在
        search_user = user.objects.filter(id=userid).exists()
        search_project = Project.objects.filter(id=projectid).exists()

        if not search_user or not search_project:
            return Response({'status': 'Fail', 'msg': '用户或项目不存在'})
        else:
            new_project_comment = project_comment()
            new_project_comment.user_id = userid
            new_project_comment.project_id = projectid
            new_project_comment.content = content
            new_project_comment.save()
            response['status'] = 'OK'
    else:
        response['status'] = 'Fail'
        if content:
            response['msg'] = '用户或项目id不可为空'
        else:
            response['msg'] = '评论不可为空'
    return Response(response)


# 查询某项目的评论
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('projectid', openapi.IN_QUERY, description="项目ID", type=openapi.TYPE_INTEGER)
    ]
)
@api_view(['GET'])
def query_project_comment(request):
    response = []
    projectid = request.GET.get('projectid')

    if projectid:
        search_project = Project.objects.filter(id=projectid).exists()
        if search_project:
            comments = project_comment.objects.filter(project_id=projectid)
            for cur_comment in comments:
                cur_user = user.objects.filter(id=cur_comment.user_id).first()  # 查找用户名

                if cur_user:
                    response.append({
                        'commentid': cur_comment.id,
                        'avatar': cur_user.avatar,
                        # 只是这样写表示需要点赞数这个值
                        'likes':3,
                        'username': cur_user.name,
                        'comment': cur_comment.content,
                    })
        else:
            return Response({'status': 'Fail','msg': '项目不存在'})
    else:
        return Response({'status': 'Fail','msg': '项目id不可为空'})
    return Response(response)


# 删除项目评论
@swagger_auto_schema(
    method='delete',
    manual_parameters=[
        openapi.Parameter('commentid', openapi.IN_QUERY, description="评论ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('userid', openapi.IN_QUERY, description="用户ID", type=openapi.TYPE_INTEGER)
    ]
)
@api_view(['DELETE'])
def delete_project_comment(request):
    commentid = request.query_params.get('commentid')
    userid = request.query_params.get('userid')
    
    if not all([commentid, userid]):
        return Response({'status': 'Fail', 'msg': '评论或用户id不可为空'})
    
    try:
        # 尝试获取评论
        cur_comment = project_comment.objects.get(id=commentid)
    except project_comment.DoesNotExist:
        #  如果没有找到评论，返回错误
        return Response({'status': 'Fail', 'msg': '评论不存在'})
    
    # 验证用户是否为评论的创建者
    if cur_comment.user_id != int(userid):
        return Response({'status': 'Fail', 'msg': '用户无删除该评论权限'})
    
    cur_comment.delete()
    
    return Response({'status': 'OK'})


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userid': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user'),
            'projectid': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the project')
        }
    )
)
# 项目点赞
@api_view(['POST'])
def like_project(request):
    response = {}

    if 'userid' not in request.data or 'projectid' not in request.data :
        return Response({'status': 'Fail', 'msg': '传参缺失'}, status=400)

    userid = request.data.get('userid')
    projectid = request.data.get('projectid')

    # 检查user和project是否存在
    user_exists = user.objects.filter(id=userid).exists()
    project_exists = Project.objects.filter(id=projectid).exists()
    if not user_exists or not project_exists:
        return Response({'status': 'Fail', 'msg': '用户或项目不存在'}, status=404)

    like_record = project_like.objects.filter(user_id=userid, project_id=projectid).first()
    if like_record:
        return Response({'status': 'Fail', 'msg': '点赞记录已存在，无法重复点赞'}, status=409)

    new_like = project_like(
        user_id=userid,
        project_id=projectid)
    new_like.save()

    cur_project = Project.objects.get(id=projectid)
    cur_project.likes += 1
    cur_project.save()

    response['status'] = 'OK'
    response['msg'] = '点赞成功'
    return Response(response)

@swagger_auto_schema(
    method='delete',
    manual_parameters=[
        openapi.Parameter('userid', openapi.IN_QUERY, description="ID of the user", type=openapi.TYPE_INTEGER),
        openapi.Parameter('projectid', openapi.IN_QUERY, description="ID of the project", type=openapi.TYPE_INTEGER)
    ]
)
# 删除项目的点赞
@api_view(['DELETE'])
def unlike_project(request):
    response = {}
    userid = request.query_params.get('userid')
    projectid = request.query_params.get('projectid')

    if not userid or not projectid:
        return Response({'status': 'Fail', 'msg': '传参缺失'}, status=400)

    # 检查user和project是否存在
    user_exists = user.objects.filter(id=userid).exists()
    project_exists = Project.objects.filter(id=projectid).exists()
    if not user_exists or not project_exists:
        return Response({'status': 'Fail', 'msg': '用户或项目不存在'}, status=404)

    # 检查点赞记录是否存在
    like_record = project_like.objects.filter(user_id=userid, project_id=projectid).first()
    if not like_record:
        return Response({'status': 'Fail', 'msg': '未查询到点赞记录'}, status=404)

    # 删除点赞记录
    like_record.delete()

    # 更新项目的点赞数
    cur_project = Project.objects.filter(id=projectid).first()
    if cur_project and cur_project.likes > 0:
        cur_project.likes -= 1
        cur_project.save()

    response['status'] = 'OK'
    response['msg'] = '成功取消点赞'
    return Response(response)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('userid', openapi.IN_QUERY, description="ID of the user", type=openapi.TYPE_INTEGER)
    ]
)
# 查看某用户所有点赞的项目
@api_view(['GET'])
def query_liked_projects(request):
    response = []
    userid = request.query_params.get('userid')
    if not userid:
        return Response({'status': 'Fail', 'msg': '传参缺失'}, status=400)

    user_exists = user.objects.filter(id=userid).exists()
    if not user_exists:
        return Response({'status': 'Fail', 'msg': '用户不存在'}, status=404)


    list_projects=project_like.objects.filter(user_id=userid)
    if not list_projects:
        response.append({'status':'Fail','msg':'该用户不存在点赞的项目'})
    else:
        response.append({'status': 'OK','msg':'获取成功'})
        for project in list_projects:
            cur_project = Project.objects.filter(id=project.project_id).first()
            if cur_project:
                response.append({
                    'id': cur_project.id,
                    'name': cur_project.name,
                    'location': cur_project.location,
                    'longitude': cur_project.longitude,
                    'latitude': cur_project.latitude,
                    'category': cur_project.category,
                    'keyword': cur_project.keyword,
                    'description': cur_project.description,
                    'likes':cur_project.likes,
                    'media':cur_project.media
                })
    return Response(response)

from fuzzywuzzy import fuzz
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('key', openapi.IN_QUERY, description="搜索内容", type=openapi.TYPE_STRING),
    ]
)
# 用户通过搜索框搜索项目
# 目前可针对项目名称、项目描述、项目位置进行模糊匹配
# 使用fuzz实现更灵活的模糊匹配，并按照匹配度降序返回
# 嵌入openai，遇到问题：使用系统解释器时可正常运行，换用虚拟环境会发生SSL/TLS协议错组，尝试将urllib3降级，没有效果
@api_view(['GET'])
def search_for_projects(request):

    key = request.query_params.get('key')
    if not key:
        return Response({'status': 'Fail', 'msg': '查询关键词缺失'}, status=400)

    # 获取所有在 UploadProject 表中存在的 project_id,避免搜索到无主的非法项目的id
    project_ids = UploadProject.objects.values_list('project_id', flat=True)
    print('project_ids', project_ids)
    # 简单模糊匹配
    # projects = Project.objects.filter(
    #     Q(id__in=project_ids), # 只搜索存在于 UploadProject 表中的项目
    #     Q(name__icontains=key) | Q(description__icontains=key) | Q(location__icontains=key)
    # )

    projects_with_score=[]
    all_projects = Project.objects.filter(id__in=project_ids)
    for cur_project in all_projects:
        # 计算匹配度
        name_score = fuzz.ratio(cur_project.name, key)
        description_score = fuzz.ratio(cur_project.description, key)
        location_score = fuzz.ratio(cur_project.location, key)

        # 选取两个字段中的最高匹配度，并二元元组形式插入
        if name_score >= 50 or description_score >= 50 or location_score >= 50:
            max_score = max(name_score, description_score, location_score)
            projects_with_score.append((cur_project, max_score))

    source = 'database'
    if projects_with_score:
        # 按匹配度降序排列
        projects_with_score.sort(key=lambda x: x[1], reverse=True)
        # 构建返回数据
        result = []
        for project,score in projects_with_score:
            # 获取项目关联的用户
            user_id = UploadProject.objects.filter(project_id=project.id).values_list('user_id', flat=True).first()
            if user_id:
                cur_user = user.objects.filter(id=user_id).first()
                print('cur_user',cur_user)

                if cur_user:
                    # 构造项目和用户信息
                    result.append({
                        'id': project.id,
                        'name': project.name,
                        'location': project.location,
                        'longitude': project.longitude,
                        'latitude': project.latitude,
                        'category': project.category,
                        'description': project.description,
                        'likes': project.likes,
                        'image': project.image,

                        'user_id': cur_user.id,
                        'user_name': cur_user.name,
                        'user_role': cur_user.role,
                        'user_avatar': cur_user.avatar
                    })
    else:
        source = 'openai'
        result = GPT_request(key)
        if not result:
            return Response({'status': 'Fail', 'msg': 'GPT生成错误'}, status=400)
    return Response({'source': source, 'data': result})

# 利用openai获取数据库中没有的项目数据
def GPT_request(prompt):
    # client = OpenAI(
    #     api_key='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',
    #     # base_url='https://api.openai.com/v1'
    # )

    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system","content": '根据以下问题，请列举3个真实存在的项目，按照以下格式列出每个项目的相关信息，回复的信息不要有开头结尾的冗余字句，经纬度以数字表示：项目名称、地点、经度、纬度、具体描述'},
    #         {"role": "user", "content": '问题：'+prompt}
    #     ]
    # )
    # generated_text = response.choices[0].message.content
    # # 测试打印gpt返回文本
    # # print("GPTtext:\n")
    # # print(generated_text)

    # # 定义正则表达式来提取信息
    # pattern = re.compile(r"""
    #     (\d+)\.\s*项目名称：(.+?)\s*
    #     地点：(.+?)\s*
    #     经度：([\d.-]+)\s*
    #     纬度：([\d.-]+)\s*
    #     具体描述：(.+?)(?:\n|$)
    # """, re.VERBOSE | re.DOTALL)

    # # 查找所有匹配项
    # matches = pattern.findall(generated_text)

    # # 将匹配项转换为字典列表
    # projects = []
    # for match in matches:
    #     project = {
    #         'id': int(match[0]),
    #         'name': match[1],
    #         'location': match[2],
    #         'longitude': float(match[3]),
    #         'latitude': float(match[4]),
    #         'description': match[5].strip()
    #     }
    #     projects.append(project)
    # return projects

    key = 'sk-ET6f5Dbdtt1A7UJ7026b2a8f858944E4AeFfC9037c11C4A4'

    client = OpenAI(
        base_url="https://api.wlai.vip/v1",
        api_key=key
    )
    
    messages=[
        {"role": "system","content":'根据以下问题，请列举5个真实存在的项目，按照以下格式列出每个项目的相关信息，每个项目前加上序号，回复的信息不要有开头结尾的冗余字句，经纬度以数字表示，具体描述不少于两百字：项目名称、地点、经度、纬度、具体描述'},
        {"role": "user", "content":'问题：'+prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    response_message = response.choices[0].message.content

    # 定义正则表达式来提取信息
    pattern = re.compile(r"""
        (\d+)\.\s*项目名称：(.+?)\s*
        地点：(.+?)\s*
        经度：([\d.-]+)\s*
        纬度：([\d.-]+)\s*
        具体描述：(.+?)(?:\n|$)
    """, re.VERBOSE | re.DOTALL)

    # 查找所有匹配项
    matches = pattern.findall(response_message)

    # 将匹配项转换为字典列表
    projects = []
    for match in matches:
        project = {
            'id': int(match[0]),
            'name': match[1],
            'location': match[2],
            'longitude': float(match[3]),
            'latitude': float(match[4]),
            'description': match[5].strip()
        }
        projects.append(project)
    
    return projects


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('key', openapi.IN_QUERY, description="搜索内容", type=openapi.TYPE_STRING),
    ]
)
# 用户通过搜索框搜索项目的提交者（也有可能没有提交项目）
# 根据用户名以及用户的area进行模糊匹配
# 使用fuzz实现更灵活的模糊匹配，并按照匹配度降序返回
@api_view(['GET'])
def search_for_users(request):

    key = request.query_params.get('key')
    if not key:
        return Response({'status': 'Fail', 'msg': '查询关键词缺失'}, status=400)

    users_with_score = []
    all_users = user.objects.all()
    for cur_user in all_users:
        # 计算匹配度
        name_score = fuzz.ratio(cur_user.name, key)
        area_score = fuzz.ratio(cur_user.area, key)
        # 选取两个字段中的最高匹配度，并二元元组形式插入
        if name_score >= 50 or area_score >= 50:
            max_score = max(name_score, area_score)
            users_with_score.append((cur_user, max_score))

    # 简单模糊匹配
    # users = user.objects.filter(
    #     Q(name__icontains=key) | Q(area__icontains=key)
    # )
    if not users_with_score:
        return Response({'status': 'Fail', 'msg': '数据库未查询到相关用户'}, status=404)

    # 按匹配度降序排序
    users_with_score.sort(key=lambda x: x[1], reverse=True)
    print('users_with_score', users_with_score)

    result = []
    for cur_user,score in users_with_score:
        cur_user = user.objects.filter(id=cur_user.id).first()
        if cur_user:
            result.append({
                'id': cur_user.id,
                'name': cur_user.name,
                'role': cur_user.role,
                'avatar': cur_user.avatar,
                'company': cur_user.company
            })
    return Response({'status': 'OK', 'data': result}, status=200)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('userid', openapi.IN_QUERY, description="用户id", type=openapi.TYPE_INTEGER)
    ]
)
# 评论组件需要
@api_view(['GET'])
def query_user_like_which(request):
    response = []
    userid = request.GET.get('userid')
    cur_user = user.objects.filter(id=userid).first()
    if cur_user:
        response.append({'status': 'OK'})
        # 查询点赞的用户ID列表
        liked_users = project_like.objects.filter(user_id=userid).values_list('project_id', flat=True)
        print(f'liked_users', list(liked_users))

        response.append({'likeIds':list(liked_users)})
    else:
        response.append({'status': 'Fail',
                         'msg': 'params invalid'})
    return Response(response)

# 获取所有项目
@swagger_auto_schema(
    method='get',
    manual_parameters=[
    ]
)
@api_view(['GET'])
def query_all_project(request):
    response = []
    project_ids = UploadProject.objects.values_list('project_id', flat=True)
    projects = Project.objects.filter(id__in=project_ids)

    if projects.exists():
        for project in projects:
            # 获取项目的作者信息
            upload_record = UploadProject.objects.filter(project=project).first()
            if upload_record:
                response.append({
                    'id': project.id,
                    'name': project.name,
                    'likes': project.likes,
                    'image': project.image,
                    'location': project.location,
                    'longitude': project.longitude,
                    'latitude': project.latitude,
                    'description': project.description,
                    'author': upload_record.user.name,
                    'avatar': upload_record.user.avatar,
                })
    else:
        return Response({'status': 'Fail', 'msg': '项目为空'}, status=404)
    return Response(response)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
       openapi.Parameter('userid', openapi.IN_QUERY, description="用户id", type=openapi.TYPE_INTEGER),
    ]
)
@api_view(['GET'])
def get_userinfo(request):
    response = {}
    userid = request.GET.get('userid')
    if not userid:
        return Response({'status': 'Fail', 'msg': '传参缺失'}, status=400)
    cur_user = user.objects.filter(id=userid).first()
    if not cur_user:
        return Response({'status': 'Fail', 'msg': '查无此人'}, status=404)

    response['userinfo'] = {
        'name': cur_user.name,
        'email':cur_user.email,
        'avatar':cur_user.avatar,
        'area':cur_user.area,
        'birthday':cur_user.birthday,
        'age':cur_user.age,
        'degree': cur_user.degree,
        'address' :cur_user.address,
        'company':cur_user.company,
        'tel':cur_user.tel,
        'style':cur_user.style,
        'url':cur_user.url,
        'direction':cur_user.direction
    }
    return Response(response)