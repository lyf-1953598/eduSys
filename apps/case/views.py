import copy
import hashlib
import os

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from .models import *
from apps.system.models import *

STATIC_URL = 'static'


# 查询地震.
@api_view(['GET'])
def query_earthquakes(request):
    response = []

    # Retrieve all earthquakes
    Earthquakes = earthquakes.objects.all()

    # Iterate over each earthquake and prepare the response
    for earthquake in Earthquakes:
        item = {}
        item['id'] = earthquake.id
        item['date'] = earthquake.date
        item['magnitude'] = earthquake.magnitude
        item['location'] = earthquake.location
        item['longitude'] = earthquake.longitude
        item['latitude'] = earthquake.latitude
        item['depth_km'] = earthquake.depth_km
        response.append(item)

    print(response)
    return Response({'status': 'OK', 'data': response})

# 查询案例
@api_view(['GET'])
def query_case(request):
    response = []
    type = request.GET.get('type')
    if type == 'excellent' or type == 'landscape' or type == 'custom':
        response.append({'status': 'OK'})
        if type == 'excellent':
            Cases = excellent_case.objects.filter()
        else:
            Cases = custome_case.objects.filter()
        for Case in Cases:
            item = {}
            item['id'] = Case.id
            item['latitude'] = Case.latitude
            item['longitude'] = Case.longitude
            item['size'] = Case.size
            if type == 'custom':
                item['date'] = Case.mid_time
                item['stage'] = 'mid'
                item['color'] = 'blue'
                response.append(item)
                item = copy.deepcopy(item)
                item['date'] = Case.term_time
                item['stage'] = 'term'
                item['color'] = 'green'
                response.append(item)
            else:
                response.append(item)
    else:
        response.append({'status': 'Fail',
                         'msg': 'type invalid'})
    print(response)
    return Response(response)


# 查询案例详情
@api_view(['GET'])
def query_case_detail(request):
    response = {}
    caseid = request.GET.get('caseid')
    type = request.GET.get('type')
    userid = request.GET.get('userid')
    if caseid and (type == 'excellent' or type == 'landscape' or type == 'custom'):
        response['status'] = 'OK'
        selfLike = False
        if like.objects.filter(caseid=caseid, userid=userid, type=type).first():
            selfLike = True
        if type == 'excellent':
            cur_case = excellent_case.objects.filter(id=caseid).first()
            response['name'] = cur_case.name
            response['url'] = cur_case.url
            response['designer'] = cur_case.designer
            response['supplier'] = cur_case.supplier
            response['address'] = cur_case.address
            response['area'] = cur_case.area
            response['description'] = cur_case.description
            response['img'] = cur_case.img
            response['type'] = 'excellent'
            response['self_like'] = selfLike
            response['size'] = cur_case.size
        else:
            cur_case = custome_case.objects.filter(id=caseid).first()
            response['name'] = cur_case.name
            response['designer'] = cur_case.designer
            response['description'] = cur_case.description
            response['address'] = cur_case.address
            response['tag'] = cur_case.tag
            response['self_like'] = selfLike
            response['size'] = cur_case.size

            stage = request.GET.get('stage')
            if stage == 'mid':
                response['time'] = cur_case.mid_time
                response['cover'] = cur_case.mid_cover
                response['img'] = cur_case.mid_album
            elif stage == 'term':
                response['time'] = cur_case.term_time
                response['cover'] = cur_case.term_cover
                response['img'] = cur_case.term_album
                response['video'] = cur_case.video
    else:
        response['status'] = 'Fail'
        response['msg'] = 'params invalid'
    return Response(response)


# 评论
@api_view(['POST'])
def make_comment(request):
    response = {}
    userid = request.data['userid']
    caseid = request.data['caseid']
    content = request.data['comment']
    type = request.data['type']
    # 先不判断id是否合法
    if content and userid and caseid:
        new_comment = comment()
        new_comment.userid = userid
        new_comment.caseid = caseid
        new_comment.content = content
        new_comment.type = type
        new_comment.save()
        response['status'] = 'OK'
    else:
        response['status'] = 'Fail'
        if content:
            response['msg'] = 'id is empty'
        else:
            response['msg'] = 'comment is empty'
    return Response(response)

@api_view(['GET'])
def query_user_like_which(request):
    response = []
    userid = request.GET.get('userid')
    cur_user = user.objects.filter(id=userid).first()
    if cur_user:
        response.append({'status': 'OK'})
        # 查询点赞的用户ID列表
        liked_users = comment_like.objects.filter(user_id=userid).values_list('comment_id', flat=True)
        print(f'liked_users', list(liked_users))

        response.append({'likeIds':list(liked_users)})
    else:
        response.append({'status': 'Fail',
                         'msg': 'params invalid'})
    return Response(response)


# 查询评论
@api_view(['GET'])
def query_comment(request):
    response = []
    caseid = request.GET.get('caseid')
    type = request.GET.get('type')

    if caseid and (type == 'excellent' or type == 'landscape' or type == 'custome'):
        response.append({'status': 'OK'})
        comments = comment.objects.filter(caseid=caseid)
        for cur_comment in comments:
            cur_user = user.objects.filter(id=cur_comment.userid).first()  # 查找用户名

            content = cur_comment.content
            if cur_user:
                # print(f'当前添加的评论id为{cur_comment.id}')
                response.append({
                    'comment_id': cur_comment.id,
                    'avatar': cur_user.avatar,
                    'username': cur_user.name,
                    'comment': content,
                    'likes':cur_comment.size,
                })
    else:
        response.append({'status': 'Fail',
                         'msg': 'params invalid'})
    return Response(response)


# 点赞
@api_view(['POST'])
def make_like(request):
    response = {}
    if 'userid' not in request.data or 'caseid' not in request.data or 'type' not in request.data:
        response['status'] = 'Fail'
        return Response(response)
    userid = request.data['userid']
    caseid = request.data['caseid']
    type = request.data['type']
    if userid and caseid and type:
        new_like = like()
        new_like.userid = userid
        new_like.caseid = caseid
        new_like.type = type
        new_like.save()
        if type == 'excellent':
            cur_case = excellent_case.objects.filter(id=caseid).first()
        else:
            cur_case = custome_case.objects.filter(id=caseid).first()
        # 更新size
        cur_case.size += 1
        cur_case.save()
        response['status'] = 'OK'
    else:
        response['status'] = 'Fail'
        response['msg'] = 'id is empty'

    return Response(response)

########################新加接口，删除点赞
@api_view(['DELETE'])
def delete_like(request):
    response = {}
    # 获取请求参数
    userid = request.data.get('userid')
    caseid = request.data.get('caseid')
    type = request.data.get('type')

    # 检查参数是否存在
    if not all([userid, caseid, type]):
        response['status'] = 'Fail'
        response['msg'] = 'Missing parameters'
    else:
        # 查找并删除点赞记录
        cur_like = like.objects.filter(userid=userid, caseid=caseid, type=type).first()
        if cur_like:
            cur_like.delete()
            # 更新对应的 case 的 size 值
            if type == 'excellent':
                cur_case = excellent_case.objects.filter(id=caseid).first()
            else:
                cur_case = custome_case.objects.filter(id=caseid).first()

            if cur_case:
                cur_case.size = max(0, cur_case.size - 1)  # 确保 size 不为负
                cur_case.save()

            response['status'] = 'OK'
        else:
            response['status'] = 'Fail'
            response['msg'] = 'Like not found'
    return Response(response)

# 新增接口，评论的点赞以及取消点赞
@api_view(['POST'])
def make_comment_like(request):
    response = {}
    # if 'userid' not in request.data or 'comment_id' not in request.data:
    #     response['status'] = 'Fail'
    #     return Response(response)
    user_id = request.data['userid']
    comment_id = request.data['comment_id']
    print(f'userid: {user_id},comment_id: {comment_id}')
    if user_id and comment_id:
        # 查找是否存在点赞记录
        cur_comment_like = comment_like.objects.filter(user_id=user_id, comment_id=comment_id)
        if cur_comment_like:
            print('将要取消点赞')
            cur_comment_like.delete()
            cur_comment = comment.objects.filter(id=comment_id).first()
            # 更新size
            cur_comment.size -= 1
            cur_comment.save()
            print('取消点赞了')
            response['status'] = 'OK'
        else:
            print('将要点赞')
            new_comment_like = comment_like()
            new_comment_like.user_id = user_id
            new_comment_like.comment_id = comment_id
            new_comment_like.save()
            cur_comment = comment.objects.filter(id=comment_id).first()
            # 更新size
            cur_comment.size += 1
            cur_comment.save()
            print('点赞了')
            response['status'] = 'OK'
    else:
        response['status'] = 'Fail'
        response['msg'] = 'id is empty'

    return Response(response)

from fuzzywuzzy import fuzz,process # 字符串查询的魔法库

# keyword查询案例
@api_view(['GET'])
def query_case_keyword(request):
    response = []
    keyword = request.GET.get('keyword')
    type =  request.GET.get('type')
    if keyword and type:
        response.append({
            'status':'OK'
        })
        if type == 'excellent':
            cases = excellent_case.objects.all()
        else:
            cases = custome_case.objects.all()
        for cur_case in cases:
            if fuzz.partial_ratio(cur_case.name,keyword) >= 50:
                response.append({
                    'id':cur_case.id,
                    'name':cur_case.name
                })
    else:
        response.append({
            'status':'Fail',
            'msg':'params invalid'
        })

    return Response(response)

# print(fuzz.partial_ratio('东方','东方明珠'))

@api_view(['POST'])
def upload_case(request):
    if request.method == 'POST':
        mid_album = []
        term_album = []

        mc = request.FILES.get("middle_cover")
        tc = request.FILES.get('term_cover')
        vd = request.FILES.get('video')
        ma = request.FILES.getlist("middle_album")
        ta = request.FILES.getlist('term_album')

        mid_cover = saveFile(mc)
        term_cover = saveFile(tc)
        video = saveFile(vd)
        for img in ma:
            mid_album.append(saveFile(img))
        for img in ta:
            term_album.append(saveFile(img))

        mid_album = genPGArray(mid_album)
        term_album = genPGArray(term_album)

        name = request.data.get('name')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        designer = request.data.get('designer')
        description = request.data.get('description')
        mid_time = request.data.get('mid_time')
        term_time = request.data.get('term_time')
        tag = '{' + request.data.get('tag') + '}'  # 可为空

        cc = custome_case.objects.filter(name=name, designer=designer)
        if cc:
            cc.update(latitude=latitude, longitude=longitude,
                      description=description, mid_time=mid_time, mid_cover=mid_cover, term_time=term_time,
                      video=video, tag=tag, mid_album=mid_album, term_album=term_album, term_cover=term_cover, size=0)
            return Response({'status': 'OK'})
        else:
            if name and latitude and longitude and designer:
                custome_case.objects.create(name=name, latitude=latitude, longitude=longitude, designer=designer,
                                            description=description, mid_time=mid_time, mid_cover=mid_cover,
                                            term_time=term_time,
                                            video=video, tag=tag, mid_album=mid_album, term_album=term_album,
                                            term_cover=term_cover, size=0)

            return Response({'status': 'OK'})
    return Response({
        'status': 'Fail',
        'msg': 'case upload failed'
    })


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


