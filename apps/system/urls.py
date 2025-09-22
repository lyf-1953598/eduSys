from .views import register,login,queryUserId,queryUserRole,updateDesigner,updateSupplier
from django.urls import path

urlpatterns = [
    path('login',login,name='login'),
    path('register',register,name='register'),
    path('user/queryRole',queryUserRole,name='queryUserRole'),
    path('user/queryId',queryUserId,name='queryUserId'),
    path('profile/designer',updateDesigner,name='updateDesigner'),
    path('profile/supplier',updateSupplier,name='updateSupplier')

]