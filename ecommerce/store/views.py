from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login , logout
from django.template.loader import render_to_string
import json 
import datetime
from .models import * 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from .forms import ProductFilterForm

def store(request):
	request_search_type = request.GET.get("searchterm")
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
		
	if (request_search_type):
		products = Product.objects.filter(name__contains=request_search_type)
	else:
		products = Product.objects.all()
	
	if request.method == 'GET':
		filter_form = ProductFilterForm(request.GET)
		if filter_form.is_valid():
			category = filter_form.cleaned_data.get('category')
			min_price = filter_form.cleaned_data.get('min_price')
			max_price = filter_form.cleaned_data.get('max_price')
			if category:
				products = products.filter(category=category)
			if min_price:
				products = products.filter(price__gte=min_price)
			if max_price:
				products = products.filter(price__lte=max_price)
		else:
			filter_form = ProductFilterForm() 

	context = {'products':products, 'cartItems':cartItems,'filter_form':filter_form}
	return render(request, 'store/store.html', context)

def filter_store(request):
	data = json.loads(request.body)
	searchterm = data['searchtearm']
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	#products = Product.objects.all()
	products = Product.objects.filter(name__contains=searchterm)
	context = {'products':products, 'cartItems':cartItems}
	#return JsonResponse('Item was added', safe=False)
	#return render(request, 'store/store.html', context)
	return JsonResponse({
      'html': render_to_string('store/store.html', context, request=request)
    })
 
def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)

def viewproduct(request , id):
	products = Product.objects.filter(id=id)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'store/viewproduct.html', context)

def userlogin(request):
	context = {}
	return render(request,'store/login.html',context)

def login_process(request):
	data = json.loads(request.body)
	username = data['form']['username']
	password = data['form']['password']
	print('Username',username)
	print('Pass',password)
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request,user)
		return JsonResponse("Success",safe=False)
	else:
		return JsonResponse("Error",safe=False)

def logout_user(request):
	logout(request)
	return JsonResponse("Success",safe=False)

def signup_form(request):
	context = {}
	return render(request,'store/signup.html',context)

def signup_process(request):
	data = json.loads(request.body)
	username = data['form']['username']
	password = data['form']['password']
	email = data['form']['email']
	user = User.objects.create_user(username, email, password)
	user.save()
	Customer.objects.create(user=user,name=username,email=email)
	if user is not None:
		return JsonResponse("Success",safe=False)
	else:
		return JsonResponse("Error",safe=False)

@api_view(['GET'])
def getdata(request):
	product = Product.objects.all()
	serializer = ProductSerializer(product,many=True)
	return Response(serializer.data)


def product_list(request):
    products = Product.objects.all()
    if request.method == 'GET':
        filter_form = ProductFilterForm(request.GET)
        if filter_form.is_valid():
            category = filter_form.cleaned_data.get('category')
            min_price = filter_form.cleaned_data.get('min_price')
            max_price = filter_form.cleaned_data.get('max_price')
            if category:
                products = products.filter(category=category)
            if min_price:
                products = products.filter(price__gte=min_price)
            if max_price:
                products = products.filter(price__lte=max_price)
    else:
        filter_form = ProductFilterForm() 
    print(filter_form)  # Print form to console for debugging
    return render(request, 'store/store.html', {'products': products, 'filter_form': filter_form})

