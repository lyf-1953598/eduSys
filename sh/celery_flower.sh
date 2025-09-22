###
 # @Descripttion: 
 # @version: 
 # @Author: shaojinxin
 # @Date: 2021-11-27 14:58:49
 # @LastEditors: shaojinxin
 # @LastEditTime: 2022-01-17 15:06:13
### 
celery -A project flower -n zhonghuanLanduse_flower.%h --address=0.0.0.0 --port=5556