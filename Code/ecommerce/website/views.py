from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import FormView
import razorpay
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Create your views here.
# Home
def homepage(request):
	categories = Categories.objects.all()
	return render(request,'index.html',{'categories':categories})

# All Products
def productall (request):
	categories = Categories.objects.all()
	products = Product.objects.all()
	return render(request,'shop-grid.html',{'products':products,'categories':categories})

# Category Products
def productCategory(request,id):
	categories = Categories.objects.all()
	categoryIs = Categories.objects.get(id = id)
	productsAre = Product.objects.filter(categories = categoryIs)
	return render(request,'shop-grid.html',{'products':productsAre, 'categories':categories, 'catname':categoryIs})

# Register
def register(request):
	if request.method == 'POST':
		form = request.POST

		first_name = form['first_name']
		email = form['email']
		password = form['password']
		mobile = form['mobile']
		address = form['address']
		try:
			user = User.objects.get(username=email)
			message = 'USERNAME ALREADY EXISTS! KINDLY LOGIN!'
			return render(request,'login.html',{'messages':message})
		except:
			useraccount = User.objects.create_user(
				username = email,
				first_name = first_name,
				email = email,
				password = password,
				)

			myuser = MyUser.objects.create(
				user = useraccount,
				mobile = mobile,
				address = address,
				account_type = 'Customer',
				)
			user = authenticate(username = email, password = password)
			login(request,user)
			return redirect('/home')
	else :
		return render(request,'login.html')

# Login
def loginUser(request):
	if request.method == 'POST':
		form = request.POST

		username = form['username']
		password = form['password']
		try:
			user = authenticate(username=username,password=password)
			print(username,password)
			if user is not None:
				login(request,user)
				myuser = MyUser.objects.get(user = user)
				if myuser.account_type=='Customer':
					return redirect('/home/')
				else:
					return redirect('/adminpage/')
			else:
				message = 'NO ACCOUNT FOUND!'
				return render(request,'login.html',{'message':message})
		except:
			message = 'INVALID USER DETAILS!'
			return render(request,'login.html',{'message':message})
	else:
		return render(request,'login.html')



# Particular Product
def productdet (request):
	return render(request,'shop-details.html')

def productsList(request,id):
 	productis = Product.objects.get(id = id)

 	try:
	 	user = request.user
	 	myuser = MyUser.objects.get(user = user)
 		sessionId = SessionMaster.objects.get(userid = myuser)
	 	return render(request,'shop-details.html',{'productis':productis,'sessionId':sessionId}) 

 	except:
	  	return render(request,'shop-details.html',{'productis':productis}) 

# Cart
@login_required(login_url='/login')	
def addtocart(request):
	user = request.user #give details of user currently loggedin
	myuser = MyUser.objects.get(user = user)

	if request.method == 'POST':
		form = request.POST

		num_product = form['num_product']
		num_id = form['num_id']
		print(num_product)

		try:	
			sessionId = form['sessionId']
			new_session = SessionMaster.objects.get(id = sessionId)
			print(sessionId)
		except:
			new_session = SessionMaster.objects.create(
			userid = myuser
			)

		#get product from models
		productis = Product.objects.get(id = num_id)

		shoppingcartis = ShoppingCart.objects.create(
			productid = productis,
			quantity = num_product,
			sessionid = new_session,
			)
		totalAmount = int(num_product)*int(productis.mrp)
		print(totalAmount)
		shoppingcartis.totalAmount = totalAmount
		shoppingcartis.save()

		return render(request,'shop-details.html',{'sessionId':new_session,'productis':productis})
	else:
		return HttpResponse('error')

# Shopping Cart
@login_required(login_url='/login')	
def shopcart(request):
	user = request.user
	myuser = MyUser.objects.get(user = user)

	try:
		sessionId = SessionMaster.objects.get(userid = myuser)
		productsToCart = ShoppingCart.objects.filter(sessionid = sessionId)
		total_cost = 0
		for x in productsToCart:
			total_cost += int(x.totalAmount)
		return render(request, 'shopping-cart.html',{'myuser':myuser,'total_cost':total_cost, 'sessionId':sessionId,'products':productsToCart})
	except:
		return render(request, 'shopping-cart.html')

# Checkout
def checkout(request):
	user = request.user
	myuser = MyUser.objects.get(user = user)

	try:
		sessionId = SessionMaster.objects.get(userid = myuser)

		orderedProducts = ShoppingCart.objects.filter(sessionid = sessionId)

		orderfinal = OrderMaster.objects.create(
			userid = myuser,
			)

		total_cost = 0
		for x in orderedProducts:
			x.ordermasterid = orderfinal
			x.sessionid = None
			x.save()

			total_cost += int(x.totalAmount)

		orderfinal.cartTotal = total_cost
		orderfinal.save()

		sessionId.delete()

		return render(request, 'checkout.html')
	except:
		return render(request, 'checkout.html')
# Account Page
def accountis(request):
	user = request.user
	myuser = MyUser.objects.get(user = user)
	orderdone = OrderMaster.objects.filter(userid = myuser)
	return render(request, 'account.html',{'myuser':myuser,'orderdone':orderdone})


# Logout
def Logout(request):
	user = request.user
	logout(request)
	return redirect('/home/')

# About
def about(request):
	return render(request,'about.html')

# For Admin
def adminPage(request):
	return render(request,'adminPage.html')

def adminCategory(request):
	categories = Categories.objects.all()
	return render(request,'categoriesadd.html',{'categories':categories})

def categoryAdd(request):
	if request.method == 'POST':
		form = request.POST

		categoryname = form['category_name'].capitalize()
		imageurl = form['image_url']
		try:
			categoryname = Categories.objects.get(name=categoryname)
			messages.warning(request, 'Category Already Exists!')
			return redirect('/categoriesadd/')
		except:
			categoryname = Categories.objects.create(
				name = categoryname,
				imageurl = imageurl,
				)
			messages.success(request, 'Category Added!')
			return redirect('/categoriesadd/')
	else :
		return redirect('/categoriesadd/')

def categoryDelete(request):
	if request.method=='POST':
		form = request.POST
		idis = form['categoryid']
		categoryis = Categories.objects.get(id = idis)
		categoryis.delete()
		messages.warning(request, 'Category Removed!')
		return redirect('/categoriesadd/')
	else:
		return redirect('/categoriesadd/')

def adminProducts(request):
	product = Product.objects.all()
	allcategory = Categories.objects.all()
	shiptime = ShipTime.objects.all()
	return render(request,'productsadd.html',{'product':product,'allcategory':allcategory,'shiptime':shiptime})

def productAdd(request):
	if request.method == 'POST':
		form = request.POST

		productname = form['product_name']
		categoryid = form['category_name']
		mrp = form['mrp']
		weight = form['weight']
		shippingtime = form['shippingtime']
		imageurl = form['image_url']

		categoryObject = Categories.objects.get(id = categoryid)
		shipObject = ShipTime.objects.get(id = shippingtime)
		try:
			productname = Product.objects.get(name=productname)
			messages.warning(request, 'Product Already Exists!')
			return redirect('/productsadd/')
		except:
			productname = Product.objects.create(
				name = productname,
				categories = categoryObject,
				mrp = mrp,
				weight = weight,
				ship = shipObject,
				imageurl = imageurl,
				)
			messages.success(request, 'Product Added!')
			return redirect('/productsadd/')
	else :
		return redirect('/productsadd/')

def productDelete(request):
	if request.method=='POST':
		form = request.POST
		idiss = form['productid']
		productis = Product.objects.get(id = idiss)
		productis.delete()
		messages.warning(request, 'Product Removed!')
		return redirect('/productsadd/')
	else:
		return redirect('/productsadd/')

def adminUsers(request):
	usersaare = MyUser.objects.all()
	return render(request,'userslist.html',{'usersaare':usersaare})

def adminOrders(request):
	orderlists = OrderMaster.objects.all().order_by('-id')
	return render(request,'orderslist.html',{'orderlists':orderlists})

def particularOrder(request,id):
	ordered = OrderMaster.objects.get(id=id)
	shopped = ShoppingCart.objects.filter(ordermasterid = ordered)
	return render(request,'order.html',{'ordered':ordered,'shopped':shopped})

def whatiOrdered(request,id):
	orderedas = OrderMaster.objects.get(id=id)
	shoppedas = ShoppingCart.objects.filter(ordermasterid = orderedas)
	return render(request,'orderedbyme.html',{'orderedas':orderedas,'shoppedas':shoppedas})

def orderDelete(request):
	if request.method=='POST':
		form = request.POST
		ids = form['orderid']
		orderis = OrderMaster.objects.get(id = ids)
		orderis.delete()
		messages.warning(request, 'Order Cancelled!')
		return redirect('/account/')
	else:
		return redirect('/account/')

def payment(request):
    if request.method == "POST":
        amount = request.POST.get('total_cost')
        

        client = razorpay.Client(
            auth=("rzp_test_HkrfPKF3F5X23O", "qQBFEp7Cuh34ZvPGteLYlmnR"))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
									
    return render(request, 'shopping-cart.html')

@csrf_exempt
def success(request):
    return render(request, "checkout.html")
