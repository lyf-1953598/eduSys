
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

### 路由

      doc/  测试友好 API 接口文档
      redoc/  开发友好 API 接口文档
      admin/  管理入口



