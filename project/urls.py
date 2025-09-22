'''
Author: shaojinxin
Date: 2022-09-14 11:01:49
LastEditTime: 2023-04-24 17:12:03
Description: 

Copyright (c) 2022 by shaojinxin/citorytech, All Rights Reserved. 
'''

from project import settings

"""metaweb URL Configuration

' urlpatterns '列表将url路由到视图。更多信息请参见:
https://docs.djangoproject.com/en/4.0/topics/http/urls/
例子:
功能视图
1. 添加一个import: from my_app导入视图
2. 在urlpatterns: path("， views. path ")中添加一个URL。家,name = '家')
基于类的观点
1. 添加一个import: from other_app。views import Home
2. 添加一个URL到urlpatterns: path("， home .as_view()， name='home')
包括另一个URLconf
1. 从django中导入include()函数。url导入包括，路径
2. 添加一个URL到urlpatterns: path('blog/'， include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

'''
description: 构建了函数，使 swagger  页面上能够选择 schema 是 http 还是 https
return {*}
'''
class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title="API文档",
        default_version='v1',
        description="时空作品集API文档",
        terms_of_service="https://www.citorytech.com",
        contact=openapi.Contact(email="citorytech@citorytech.com"),
        # license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    # url='https://metaweb.citory.tech/', # Important bit
    generator_class=BothHttpAndHttpsSchemaGenerator, # swagger  页面上能够选择 schema 是 http 还是 https
    permission_classes=(permissions.AllowAny,),
)
admin.site.site_title = 'metaweb'
 
admin.site.site_header = '元时空引擎—时空作品集'

urlpatterns = [
    # 对测试人员更友好
    path('MetaWebApi/web/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # 对开发人员更友好
    path('MetaWebApi/web/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # 管理界面
    path('MetaWebApi/web/admin/', admin.site.urls),
    path('api/MetaWebApi/web/enroll/', include('apps.enroll.urls')),
    path('MetaWebApi/web/dashboard/', include('apps.dashboard.urls')),
    # path('metaweb/register',  views.register),
    path('api/v1/case/',include('apps.case.urls')),
    path('api/v1/',include('apps.system.urls')),
    # re_path(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT },name="media"),
]
