###
 # @Descripttion: 
 # @version: 
 # @Author: shaojinxin
 # @Date: 2022-01-13 15:10:08
 # @LastEditors: shaojinxin
 # @LastEditTime: 2022-01-17 15:06:35
### 
celery -A project worker -n zhonghuanLanduse.%h  -l info
