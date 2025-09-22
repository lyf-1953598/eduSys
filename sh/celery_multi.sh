###
 # @Descripttion: 
 # @version: 
 # @Author: shaojinxin
 # @Date: 2021-11-27 14:03:38
 # @LastEditors: shaojinxin
 # @LastEditTime: 2022-01-17 15:06:32
### 
celery multi restart -A project worker -n zhonghuanLanduse.%h  -c 10 -l info --logfile=logs/%h.log --pidfile=logs/%h_pid.text