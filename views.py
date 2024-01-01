from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Cart


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop.html', {'products': products})

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        # other logic...
        return render(request, 'productdetail.html', {'product': product})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product does not exist.")
            return redirect('addtocart.html')

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f"Added {quantity} {product.title}(s) to your cart.")

        # Redirect to a different URL after adding to the cart
        return redirect('cart_summary')  # Replace 'cart_summary' with the actual URL name

    # Render the 'addtocart.html' template if it's a GET request
    return render(request, 'addtocart.html')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
            return render(request, 'addtocart.html', {'carts': cart, 'amount': amount, 'totalamount': totalamount, 'totalitem': totalitem})
        else:
            return render(request, 'emptycart.html', {'totalitem': totalitem})
    else:
        return render(request, 'emptycart.html', {'totalitem': totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'checkout.html', {'add': add, 'cart_items': cart_items, 'totalcost': totalamount})

@login_required
def payment_done(request):
    custid = request.GET.get('custid')
    print("Customer ID", custid)
    user = request.user
    cartid = Cart.objects.filter(user=user)
    customer = Customer.objects.get(id=custid)
    print(customer)
    for cid in cartid:
        OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
        print("Order Saved")
        cid.delete()
        print("Cart Item Deleted")
    return redirect("orders")

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")

@login_required
def address(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	add = Customer.objects.filter(user=request.user)
	return render(request, 'address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
	op = OrderPlaced.objects.filter(user=request.user)
	return render(request, 'orders.html', {'order_placed':op})

def category(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			categorys = Product.objects.filter(category='C')
	elif data == 'Mens' or data == 'Womens':
			categorys = Product.objects.filter(category='M').filter(brand=data)
	elif data == 'below':
			categorys = Product.objects.filter(category='W').filter(discounted_price__lt=10000)
	elif data == 'above':
			categorys = Product.objects.filter(category='C').filter(discounted_price__gt=10000)
	return render(request, 'shop.html', {'categorys':categorys, 'totalitem':totalitem})


class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'register.html', {'form':form})
  
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
  return render(request, 'register.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

def product_detail(request, product_slug):
    # Define product data in a list of dictionaries or a database model
    products = {
        'Luxury Perfume GiftSet For Women': {'id': 8, 'title': 'Luxury Perfume GiftSet For Women', 'selling_price': 565, 'product_image': 'productimg/img1.webp'},
        'tomato': {'id': 2, 'title': 'Tomato', 'selling_price': 30, 'product_image': 'productimg/product-5.jpg'},
        'apple': {'id': 3, 'title': 'Apple', 'selling_price': 25, 'product_image': 'images/product_01.jpg'},
        'orange': {'id': 4, 'title': 'Orange', 'selling_price': 45, 'product_image': 'images/orange.jpg'},
    }

    # Try to fetch the product using the product_slug
    product = products.get(product_slug)

    # If product doesn't exist, return a 404 page
    if not product:
        return render(request, '404.html')

    # Create a context dictionary to pass to the template
    context = {
        'product': product,
    }

    return render(request, 'productdetail.html', context)

def index(request):
    # your view logic here
    return render(request, 'index.html')

def about(request):
  
  return render(request,'about.html')



def mens(request):
  
  return render(request,'mens.html')

def womens(request):
  
  return render(request,'womens.html')

def contact(request):
  
  return render(request,'contact.html')

def shop(request):
  
  return render(request,'shop.html')

def cart(request):
  
  return render(request,'cart.html')

def login(request):
  
  return render(request,'login.html')

def register(request):
  
  return render(request,'register.html')

def logout(request):
  
  return render(request,'logout.html')

