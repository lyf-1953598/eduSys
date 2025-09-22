from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class user(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    area = models.CharField("所在地区",max_length=20,null=True,blank=True)
    birthday = models.DateField("生日",null=True,blank=True)
    age = models.IntegerField("年龄",null=True,blank=True)
    degree = models.CharField("学位",max_length=20,null=True,blank=True)
    address = models.CharField("地址",max_length=50,null=True,blank=True)
    company = models.CharField("公司",max_length=50,null=True,blank=True)
    tel = models.CharField("电话",max_length=15,null=True,blank=True)
    style = models.TextField("风格",null=True,blank=True)
    url = models.CharField("个人主页",max_length=100,null=True,blank=True)
    attachment = ArrayField(models.CharField("附件",max_length=32),null=True,blank=True)
    direction = models.CharField("商务方向",max_length=50,null=True,blank=True)

class customer(models.Model):
    customer = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True)

class supplier(models.Model):
    supplier = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True)
    product_description = models.TextField("产品介绍", null=True, blank=True)

class designer(models.Model):
    designer = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True)
    personal_description = models.TextField("个人介绍")
    portfolio_link = models.URLField("作品集链接")

class cus_sup_communication(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    sender = models.CharField(max_length=50)

class cus_sup_follow(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE)
    followed_time = models.DateTimeField(auto_now_add=True)

class cus_des_communication(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    designer = models.ForeignKey(designer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    sender = models.CharField(max_length=50)

class cus_des_follow(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    designer = models.ForeignKey(designer, on_delete=models.CASCADE)
    followed_time = models.DateTimeField(auto_now_add=True)
class product(models.Model):
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=500)
    listed_time = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)

class browse_product(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    browse_time = models.DateTimeField(auto_now_add=True)

class add_product_to_favorite(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)  # 可选的个人备注

class add_product_to_cart(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

class product_review(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    image = models.CharField(max_length=500)
    added_time = models.DateTimeField(auto_now_add=True)

class order(models.Model):
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()

class logistics_information(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    logistics_company = models.CharField(max_length=255)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

class project(models.Model):
    designer = models.ForeignKey(designer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

class browse_project(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    browse_time = models.DateTimeField(auto_now_add=True)

class add_project_to_favorite(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)  # 可选的个人备注

class project_review(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    added_time = models.DateTimeField(auto_now_add=True)

class contract(models.Model):
    designer = models.ForeignKey(designer, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    #supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    content = models.TextField()

class quotation(models.Model):
    designer = models.ForeignKey(designer, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    # supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
