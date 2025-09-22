import hashlib
import os

from django.shortcuts import render,HttpResponse

from project import settings
from .models import user
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
STATIC_URL = 'static'
# Create your views here.

@api_view(['POST'])
def login(request):
    response = {}
    if request.method == 'POST' and 'name' in request.data and 'role' in request.data:
        name = request.data['name']
        role = request.data['role']
        avatar = request.data['avatar']
        corr_user = user.objects.filter(name=name, role=role).first()  # 查数据库得到邮箱
        if not corr_user:
            for role in ['designer', 'owner', 'supplier']:
                user.objects.create(name=name, role=role, avatar=avatar)
        corr_user = user.objects.filter(name=name, role=role).first()
        response['id'] = corr_user.id
        return Response(response)
    # return Response({
    #     'status': 'BAD',
    #     'msg': 'login failed'
    # })

@api_view(['POST'])
def register(request):
    response = {}
    if request.method == 'POST' and 'name' in request.data and 'password' in request.data and 'role' in request.data \
            and 'email' in request.data:
        name = request.data['name']
        password = request.data['password']
        role = request.data['role']
        email = request.data['email']

        user.objects.create(name=name,email=email,password=password,role=role)
        corr_user = user.objects.filter(email=email).first()
        response["status"] = "OK"
        response['id'] = corr_user.id
        response['name'] = name
        response['email'] = email
        response['password'] = password
        response['role'] = role
        return Response(response)
    return Response({
        'status':'BAD',
        'msg':'register failed'
    })


@api_view(['GET'])
def queryUserRole(request):
    response = []
    role = request.GET.get('role')
    # 按照role查找
    if role == 'designer':
        response.append({'status': 'OK'})
        users = models.user.objects.filter(role=role)
        for user in users:
            item = {}
            item['id'] = user.id
            item['name'] = user.name
            item['email'] = user.email
            item['area'] = user.area
            item['style'] = user.style
            item['tel'] = user.tel
            item['url'] = user.url
            item['avatar'] = user.avatar
            response.append(item)
    elif role == 'supplier':
        response.append({'status': 'OK'})
        users = models.user.objects.filter(role=role)
        for user in users:
            item = {}
            item['id'] = user.id
            item['name'] = user.name
            item['direction'] = user.direction
            item['url'] = user.url
            item['avatar'] = user.avatar
            response.append(item)
    else:
        response.append({'status': 'Fail',
                         'msg': 'role invalid'})
    return Response(response)

@api_view(['GET'])
def queryUserId(request):
    response = []
    userId = request.GET.get('userid')
    if userId:  # 按照userId查找
        user = models.user.objects.filter(id=userId)
        if len(user):  # 查找到了
            user = user.first()
            if user.role == 'designer':
                response.append({'status': 'OK'})
                item = {}
                item['id'] = user.id
                item['name'] = user.name
                item['email'] = user.email
                item['area'] = user.area
                item['birthday'] = user.birthday
                item['age'] = user.age
                item['degree'] = user.degree
                item['address'] = user.address
                item['company'] = user.company
                item['style'] = user.style
                item['tel'] = user.tel
                item['url'] = user.url
                item['avatar'] = user.avatar
                response.append(item)
                return Response(response)
            elif user.role == 'supplier':
                response.append({'status': 'OK'})
                item = {}
                item['id'] = user.id
                item['name'] = user.name
                item['attachment'] = user.attachment
                item['direction'] = user.direction
                item['url'] = user.url
                item['avatar'] = user.avatar
                response.append(item)
                return Response(response)
    return Response({'status': 'Fail',
            'msg': 'userid invalid'})

@api_view(['POST'])
def updateDesigner(request):
    if 'id' in request.data:
        user = models.user.objects.filter(id=request.data['id'])  # 查找user
        user = user.first()
        if user and user.role=='designer':
            user.__dict__.update(**request.data)
            user.save()
            return Response({'status':'OK'})
        return Response({'status':'Fail',
                'msg':'userid invalid'})
    return Response({'status':'Fail',
            'msg':'can\'t get userid'})


@api_view(['POST'])
def updateSupplier(request):
    if 'id' in request.data:
        user = models.user.objects.filter(id=request.data['id'])  # 查找user
        if user:
            attchs = []
            files = request.FILES.getlist('attachment')
            for file in files:
                attchs.append(saveFile(file))
            attachment = genPGArray(attchs)
            name = request.data.get('name')
            url = request.data.get('url')
            direction = request.data.get('direction')
            user.update(name=name, url=url, direction=direction, attachment=attachment)
            return Response({'status':'OK'})
    return Response({'status':'Fail',
            'msg':'can\'t get userid'})

def genPGArray(arr):
    if len(arr) == 0:
        return '{}'
    ret = '{'
    for str in arr:
        ret += settings.STATIC_URL
        ret += str
        ret += ','
    ret = ret[:-1]
    ret += '}'
    return ret

def saveFile(file):
    if not file:
        return ''
    # md5重命名
    md5obj = hashlib.md5()
    md5obj.update(file.read())
    hash = md5obj.hexdigest()
    formatname = str(hash)[:5] + '_' + file.name

    # 保存位置
    inner_path = os.path.join(settings.LOCAL_DIR, STATIC_URL, formatname)
    destination = open(inner_path, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    return formatname