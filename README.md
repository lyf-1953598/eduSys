<!--
 * @Descripttion: 
 * @version: 
 * @Author: shaojinxin
 * @Date: 2021-11-26 14:54:50
 * @LastEditors: shaojinxin shaojinxin@citorytech.com
 * @LastEditTime: 2023-04-24 17:29:11
-->
[回到首页](../README.md)

## 仓库基本情况
### 相关背景
> 本工程为元时空引擎—时空作品集的Django后端

### 安装使用

1. 将仓库复制到本地(git clone时请输入自己相应的账户和密码)，并使用VScode或者Hbuilder打开
```shell
    git clone https://git.citorytech.com/shaojinxin/metaweb_backend.git
```
2. 环境(conda/docker)
```shell
		python = 3.6
```
3. 安装依赖

```shell
		pip install -r requirements.txt
```

5. 启动Django
```shell
    sh sh/start.sh
```
6. 启动 celery 默认队列
```shell
    sh sh/celery_multi.sh
```
7. 启动批量任务的单例队列：
```shell
    sh sh/celery_multi_queue_a.sh
```
8. 启动celery 监控程序
```shell
		sh sh/celery_flower.sh
```
9. 启动celery 定时任务
```shell
		sh sh/celery_beat.sh
```
### 本机数据库连接方法（针对暑期专业实习）
#### 1.本机下载PostgreSQL,并创建一个新的数据库
#### 2.修改project/settings.py中关于连接数据库的配置
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "OPTIONS": {
            "options": "-c search_path=public"
        },
        'NAME': 'postgres',  # 数据库名字
        'USER': 'postgres',  # 用户名
        "PASSWORD": 'password',  # 自己的密码
        "HOST": 'localhost',
        'PORT': 5432,
    },
}

```
#### 3.在后端代码的终端运行数据库迁移命令
```
python manage.py migrate
```
#### 4.可选地使用datagrip,navicat等图形化数据库
#### 5.运行python manage.py runserver 0.0.0.0:6614即可连接数据库

### 当前项目部署位置

```
05工作站
- 项目地址：/home/shaojinxin/data/server/metaweb/
- 用户：shaojinxin
- 进程守护：supervisor
```
### 项目架构
    ├─apps          
    │  ├─webserver          //  网络服务
    ├─logs              // 日志
    ├─java              //  胡文亮的 java 实现参考
    ├─sh              //    shell文件
    ├─project          //项目配置文件
    │  └─celeryconfig.py          //celery配置文件,定义 broker、queues 等
    ├─用地配平.md              //   用地配平需求
    ├─地块生成.sql              //    初始未配平的地块生成 sql 代码
    └─logs          // 日志，自动按天分割，保留最近30天

### 路由

      doc/  测试友好 API 接口文档
      redoc/  开发友好 API 接口文档
      admin/  管理入口



