# -*- coding=utf-8
'''
Descripttion: 全局函数
version: 
Author: shaojinxin
Date: 2022-01-17 17:02:42
LastEditors: shaojinxin shaojinxin@citorytech.com
LastEditTime: 2023-04-24 17:23:40
'''

'''
腾讯云 COS 配置
'''
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = ''     # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
secret_key = ''   # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
region = ''      # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                # COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
endpoint = '' # 替换为用户的 endpoint 或者 cos全局加速域名，如果使用桶的全球加速域名，需要先开启桶的全球加速功能，请参见https://cloud.tencent.com/document/product/436/38864

token = None               # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
# config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Endpoint=endpoint, Scheme=scheme)
# cosclient = CosS3Client(config)



import os,time,logging
from logging import handlers
def _logging(**kwargs):
    level = kwargs.pop('level', None)
    filename = kwargs.pop('filename', None)
    datefmt = kwargs.pop('datefmt', None)
    format = kwargs.pop('format', None)
    if level is None:
        level = logging.DEBUG
    if filename is None:
        filename = 'default.log'
    if datefmt is None:
        datefmt = '%Y-%m-%d %H:%M:%S'
    if format is None:
        format = '%(asctime)s [%(module)s] %(levelname)s [%(lineno)d] %(message)s'

    log = logging.getLogger(filename)
    format_str = logging.Formatter(format, datefmt)

    def namer(filename):
        return filename.split('default.')[1]

    cmd = logging.StreamHandler()
    cmd.setFormatter(format_str)
    cmd.setLevel(level)
    log.addHandler(cmd)

    th = handlers.TimedRotatingFileHandler(filename=filename, when='midnight',interval=1, backupCount=30, encoding='utf-8')
    # th.namer = namer
    th.suffix = "%Y-%m-%d.log"
    th.setFormatter(format_str)
    th.setLevel(logging.INFO)
    log.addHandler(th)
    log.setLevel(level)
    return log
os.makedirs('./logs', exist_ok=True)

null=None
# Create your models here.
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

'''
Descripttion: 对一个包含重复项的 list 转化为 item:count 的 dict
TODO: 
param {ARRAY} mylist
return {DICT}
'''
def list2countdic(mylist):
    mydic = {}
    for item in mylist:
        if item not in mydic.keys():
            mydic[item]=1
        else:
            mydic[item]+=1
    mycount = sorted(mydic.items(),key = lambda i: i[1],reverse=True)
    return dict(i for i in mycount)


