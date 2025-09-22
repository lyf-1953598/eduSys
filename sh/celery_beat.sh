###
 # @Descripttion: 启动beat 调度器使用数据库。仅在一台永久在线的终端启用即可。
 # @version: 
 # @Author: shaojinxin
 # @Date: 2021-12-15 17:02:09
 # @LastEditors: shaojinxin
 # @LastEditTime: 2022-01-13 15:22:41
### 
celery -A project beat  -l info --logfile=logs/Beat.log --pidfile=logs/Beat_pid.text --scheduler django_celery_beat.schedulers:DatabaseScheduler