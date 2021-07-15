from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyUser(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
	mobile = models.CharField(max_length=10, null = True, blank = True)
	address = models.CharField(max_length=500, null = True, blank = True)
	account_type = models.CharField(max_length = 100, null = True, blank = True)
	def __str__(self):
		return '%s' %(self.mobile)

class Categories(models.Model):
	name = models.CharField(max_length=100, null = True, blank = True)
	imageurl = models.URLField(null = True, blank = True)
	def __str__(self):
		return '%s' %(self.name)

class ShipTime(models.Model):
	name = models.CharField(max_length=100, null = True, blank = True)
	def __str__(self):
		return '%s' %(self.name)

class Product(models.Model):
	name = models.CharField(max_length=100, null= True, blank = True)
	categories = models.ForeignKey(Categories, on_delete = models.CASCADE, null = True, blank = True)
	mrp = models.CharField(max_length=10, null= True, blank = True)
	ship = models.ForeignKey(ShipTime, on_delete = models.CASCADE, null = True, blank = True)
	imageurl = models.URLField(null = True, blank = True)
	def __str__(self):
		return '%s' %(self.name)

class SessionMaster(models.Model):
	userid = models.ForeignKey(MyUser, on_delete = models.CASCADE, null = True, blank =True)	
	ordertimedate = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return '%s' %(self.userid)

class OrderMaster(models.Model):
	userid = models.ForeignKey(MyUser, on_delete = models.CASCADE, null = True, blank =True)	
	ordertimedate = models.DateTimeField(auto_now_add = True)
	order_status = models.BooleanField(default = True)
	cartTotal = models.CharField(max_length = 20, null = True, blank = True)
	payment_id= models.CharField(max_length=100, null=True)
	
class ShoppingCart(models.Model):
	productid = models.ForeignKey(Product, on_delete = models.CASCADE, null = True, blank = True)
	quantity = models.IntegerField(default = 1)
	totalAmount = models.CharField(max_length = 20, null = True, blank = True)
	sessionid = models.ForeignKey(SessionMaster, on_delete = models.CASCADE, null = True, blank = True)
	ordermasterid = models.ForeignKey(OrderMaster, on_delete = models.CASCADE, null = True, blank = True)
	# payment_id= models.CharField(max_length=100)
	# paid=models.BooleanField(default=False)
	def __str__(self):
		return '%s' %(self.productid)

# class payment(models.Model):
# 	productid = models.ForeignKey(Product, on_delete = models.CASCADE, null = True, blank = True)
# 	totalAmount = models.CharField(max_length = 20, null = True, blank = True)
	
# 	paid=models.BooleanField(default=False)
