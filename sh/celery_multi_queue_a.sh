###
 # @Descripttion: 
 # @version: 
 # @Author: shaojinxin
 # @Date: 2021-12-01 17:23:12
 # @LastEditors: shaojinxin
 # @LastEditTime: 2022-01-17 15:06:26
### 
celery multi restart -A project worker -n zhonghuanLanduse_queue_a.%h  -c 1  -Ofair -B -Q queue_a -l info --logfile=logs/%h.log --pidfile=logs/%h_pid.text 