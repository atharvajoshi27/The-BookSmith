from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
# from django.contrib.auth import is_authenticated
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from .forms import CreateUser, AddBook

# Create your views here.

# references :
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

def index(request):
	return render(request, 'Store/home_page.html')


def register(request):
	if request.method == "POST":
		# print(request.POST)
		
		form = CreateUser(request.POST)
		print(type(form))
		for key in form:
			print(key, ": ", key.errors)
		# instance = form.save()
		if form.is_valid():
			print("FORM IS VALID")
			
			# Saving details of new user
			# I tried doing form.save() but it wasn't hashing password

			instance = User.objects.create_user(**form.cleaned_data)
			
			print(instance.__dict__)

			# Linking to vendor or customer model
			is_vendor = instance.is_vendor
			if is_vendor:
				new_vendor = Vendor()
				new_vendor.vendor_details = instance
				new_vendor.save()
			else:
				new_customer = Customer()
				new_customer.customer_details = instance
				new_customer.save()
			return HttpResponse("<b>User Created Successfully</b>")
		else:
			print("Form is invalid")
			context = {
			"form" : form,
			}
			return render(request, 'Store/register.html', context)
	else:
		form = CreateUser()
		context = {
		"form" : form,
		}
		return render(request, 'Store/register.html', context)


def log_in(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			# return HttpResponse(f"<b>{user.username} logged in </b>")
			if user.is_vendor:
				# vendor = user.vendor_set.first()
				# books = vendor.book_set.all()
				# context = {
				# 	"books" : books,
				# }
				# return render(request, 'Store/index_vendor.html', context=context)
				return HttpResponseRedirect(reverse('index-vendor'))
			else:
				# books = Book.objects.all()
				# context = {
				# 	"books" : books,
				# }
				# return render(request, 'Store/index_customer.html', context)
				return HttpResponseRedirect(reverse('index-customer'))
		
		else:
			context = {
				"message" : "Invalid username and/or password",
			}

			return render(request, 'Store/login.html', context)
		pass
	else:
		return render(request, "Store/login.html")


@login_required
def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def index_customer(request):
	# user = request.user
	# if user.is_vendor:
	# 	return HttpResponseRedirect(reverse('index-vendor'))

	# cats = {}

	# categories = Category.objects.all()
	
	# for category in categories:
	# 	print(category.book_set)
	# 	# If book set is not empty
	# 	books = Book.objects.filter(category=category).order_by("-date")[:9]
	# 	if bool(books):
	# 		cats[category.category] = books
	# 		print(cats[category.category])

	# # books = Book.objects.filter(category=).order_by("-date").all()

	# # print(f"Type of books : {type(books)}")
	# context = {
	# 	"categories" : cats,
	# }
	# return render(request, 'Store/index_customer.html', context)

	user = request.user
	if user.is_vendor:
		return HttpResponseRedirect(reverse('index-vendor'))

	cats = []

	categories = Category.objects.all()

	for category in categories:
		if category.book_set.all().exists():
			cats.append(category)
	
	# books = Book.objects.filter(category=).order_by("-date").all()

	# print(f"Type of books : {type(books)}")
	context = {
		"categories" : cats,
	}
	return render(request, 'Store/categories.html', context)

@login_required
def index_vendor(request):
	user = request.user
	if not user.is_vendor:
		return HttpResponseRedirect(reverse('index-customer'))

	vendor = user.vendor_set.first()
	books = vendor.book_set.all()
	context = {
		"books" : books,
	}
	return render(request, 'Store/index_vendor.html', context=context)

@login_required
def addbook(request):
	user = request.user
	if not user.is_vendor:
		return HttpResponseRedirect(reverse('index-customer'))
	if request.method == "POST":
		print("Request : ", request.POST)
		form = AddBook(request.POST, request.FILES)
		try:
			if form.is_valid():
				print("Form Validated")

				# Don't commit because we need to assign vendor, category
				# Also we need to change the name of image uploaded
				instance = form.save(commit=False)
				print("Instance commit False : ", instance)
				category_name = request.POST.get('category')

				# If category exists already
				obj = Category.objects.filter(category=category_name).first()

				# If doesn't exist, create one
				if obj is None:
					obj = Category(category=category_name)
					obj.save()

				# Assign category to instance
				instance.category = obj

				# Logged in user is a part of User class, to get the corresponding vendor :
				vendor = request.user.vendor_set.first()
				instance.vendor = vendor

				instance.save()
				return HttpResponse("<b>Valid Form and Book Added!</b>")

			else:
				form = AddBook(request.POST, request.FILES)
				context = {
					"form" : form,
					"message" : "Inavlid Input. Please Fill All Details Correctly."
				}
				return render(request, 'Store/addbook.html', context)
		except Exception as e:
			context = {
				"form" : form,
				"message" : "Some Error Occurred. Try Again."
			}
			print(f"Exception {e} Occurred.")
			return render(request, 'Store/addbook.html', context)

	else:
		form = AddBook()
		context = {
		"form" : form,
		}
		return render(request, 'Store/addbook.html', context)

@login_required
def cart_item(request, book_id):
	print(f"Book Id: {book_id} : {type(book_id)}")
	try:
		book_id = int(book_id)
		book = Book.objects.filter(pk=book_id).first()
		user = request.user
		cart = user.cart_set.first()
		print("Step 1")
		if not cart is None:
			print("Step 1.1")
			yes = False
			for cart_item in cart.cartitem_set.all():
				print("Step 1.2")
				print(f"b_id = {cart_item.book_id.book_id}")
				if cart_item.book_id.book_id == book_id:
					print("Step 1.3")
					cart_item.book_quantity = cart_item.book_quantity + 1
					cart_item.save()
					messages.success(request, "Item Added")
					yes = True
					break
			if not yes:
				print("Step 1.4")
				cart_item = CartItem(book_quantity=1, book_id=book, cart=cart)
				cart_item.save()
				messages.success(request, "Item Added")
			print("Step 2")

		else:
			print("Step 2.1")
			cart_item = CartItem(book_quantity=1, book_id=book)
			# cart_item.save(commit=False)
			print("Step 2.2")
		print("Step 3")
		if cart is None:
			cart = Cart(customer_id=user)
			cart.save()
			cart_item.cart = cart
			cart_item.save()
			messages.success(request, "Item Added")

		print("Step 4")

		if user.is_vendor:
			return HttpResponseRedirect(reverse('cart-vendor'))
		else:
			return HttpResponseRedirect(reverse('cart-customer'))
		print("Step 5")
	except Exception as e:
		print(f"Exception {e} occurred in cart_item.")
		context = {
			"message" : "Requested item is currently out of stock."
		}
		raise Http404('Something Went Wrong.')

@login_required
def cart_view(request):
	user = request.user
	
	context = {
		"cart_exists" : True,
	}

	cart = user.cart_set.first()
	total = 0
	# Cart for the user has been created
	if not cart is None:
		cart_items = cart.cartitem_set.all()
		for cartitem in cart_items:
			total += cartitem.book_quantity * cartitem.book_id.book_price

		# If hasn't added any cartitem
		if not bool(cart_items):
			context["cart_exists"] = False

		# If cart is populated
		else:
			context["cart_exists"] = True
			context["cart_items"] = cart_items
	
	# Never added any cartitem
	else:
		context["cart_exists"] = False
	
	context["total"] = total
	return render(request, 'Store/cart.html', context)


@login_required
def cart_remove(request, cart_item):
	cart_item = int(cart_item)
	item = CartItem.objects.filter(pk=cart_item).first()

	# item must exist
	
	if not item is None:
		# item must belong to its creator
		if item.cart.customer_id != request.user:
			messages.warning(request, 'Item Cannot Be Deleted')
			pass
		else:
			item.delete()
			messages.success(request, 'Item Deleted')
	else:
		messages.warning(request, 'Item Cannot Be Deleted')

	if request.user.is_vendor:
		# x = reverse('cart-vendor')
		# print(x)
		return redirect(reverse('cart-vendor'))
	
	else:
		# x = reverse('cart-customer')
		# print(x)
		return redirect(reverse('cart-customer'))

@login_required
def cart_update(request):
	user = request.user
	if request.method == "POST":
		# print(request.POST)
		# cartitem_ids = request.POST["cartitem_ids"]
		quantity = request.POST.getlist("quantity")
		# for cartitem_id in cartitem_ids:
		# 	cartitem = 
		cart = request.user.cart_set.first()
		
		p = 0
		# print(f"CARTITEMS has length : {len(cartitems)} ", cartitems)
		# print(f"QUANTITY has length : {len(quantity)} ", quantity)
		try :
			cartitems = cart.cartitem_set.all()
			for cartitem in cartitems:
				# print("HELLO")
				q = int(quantity[p])
				if q > 0:
					cartitem.book_quantity = q
					cartitem.save()
				else:
					cartitem.delete()
				p += 1

			messages.success(request, "Cart Updated")
		except Exception as e:
			messages.warning(request, "Cart Cannot Be Updated")
	
	if user.is_vendor:
		next = reverse('cart-vendor')
	else:
		next = reverse('cart-customer')

	return HttpResponseRedirect(next)


@login_required
def category_details(request, category):
	category = Category.objects.filter(category=category).first()
	if not category is None:
		books = category.book_set.all()
		context = {
			"category" : category.category,
			"books" : books,
		}
		return render(request, 'Store/category.html', context)

	else:
		raise Http404(request, "No Such Category")
	pass

@login_required
def payment(request):

	# payment_choices = (
	# 	('CC', 'Credit Card'),
	# 	('DC', 'Debit Card'),
	# 	('NB', 'Net Banking'),
	# 	('GP', 'Google Pay'),
	# )
	# payment_id = models.AutoField(primary_key=True)
	# payment_type = models.CharField(max_length=4, choices=payment_choices)
	# amount = models.DecimalField(max_digits=6, decimal_places=2)
	# payment_date = models.DateTimeField(auto_now_add=True)
	# cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	# customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
	user = request.user

	if request.method == "POST":
		print("Payment Received")
		paymentmethod = request.POST["paymentMethod"]
		pay = Payment()
		if paymentmethod == "Credit Card":
			pay.payment_type = "CC"
			# pay = Payment(payment_type="CC")
		elif paymentmethod == "Debit Card":
			pay.payment_type = "DC"
			# pay = Payment(payment_type="CC")
		elif paymentmethod == "Net Banking":
			pay.payment_type = "NB"
			# pay = Payment(payment_type="NB")
		else :
			pay.payment_type = "GP"
			# pay = Payment(payment_type="GP")

		pay.amount = request.POST["grand_total"]
		pay.customer_id = user

		cart = user.cart_set.first()
		cart.delete()
		pay.save()
		messages.success(request, "Payment Done For Your Cart. You Will Be Delivered Soon. Thanks.")
		# pay.cart = 
		if user.is_vendor:
			return HttpResponseRedirect(reverse('index-vendor'))
		else:
			return HttpResponseRedirect(reverse('index-customer'))
		# return HttpResponseRedirect()
		pass
	else:
		try :
			cart = user.cart_set.first()
			cartitems = cart.cartitem_set.all()
			details = []
			grand_total = 0
			items = 0
			for cartitem in cartitems:
				l = []
				book_name = cartitem.book_id.book_name
				if cartitem.book_quantity > cartitem.book_id.book_quantity:
					messages.warning(request, f'{cartitem.book_id.book_name} Is Unavailable')
					if user.is_vendor:
						return HttpResponseRedirect(reverse('cart-vendor'))
					else:
						return HttpResponseRedirect(reverse('cart-customer'))
					# return HttpResponseRedirect(reverse('cart'))
				price = cartitem.book_quantity * cartitem.book_id.book_price
				l.append(book_name)
				l.append(price)
				l.append(cartitem.book_id.book_author)
				grand_total += price
				items += 1
				details.append(l)
		
			context = {
				"details" : details,
				"grand_total" : grand_total,
				"items" : items,
			}

			return render(request, 'Store/payment.html', context)
		except Exception as e:
			messages.warning(request, "Add Something To Cart First.")
			if user.is_vendor:
				return HttpResponseRedirect(reverse('cart-vendor'))
			else:
				return HttpResponseRedirect(reverse('cart-customer'))

def book_details(request, book_id):
	book_id = int(book_id)
	book = Book.objects.filter(pk=book_id).first()
	if not book is None:
		context = {
			"book" : book,
		}
		return render(request, 'Store/book_details.html', context)
	else:
		raise Http404(request, 'Book Not Found')
