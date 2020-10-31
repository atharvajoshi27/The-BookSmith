from django.urls import path
from . import views



urlpatterns = [

	path('', views.index, name='index'),
	path('register', views.register, name='register'),
	path('login', views.log_in, name='login'),
	path('logout', views.log_out, name='logout'),
	path('vendor/addbook', views.addbook, name='addbook'),
	path('vendor/index', views.index_vendor, name='index-vendor'), 
	path('customer/index', views.index_customer, name='index-customer'),
	path('customer/addtocart/<int:book_id>', views.cart_item, name='cart-item'),
	path('customer/cart', views.cart_view, name='cart-customer'),
	path('vendor/cart', views.cart_view, name='cart-vendor'),
]

