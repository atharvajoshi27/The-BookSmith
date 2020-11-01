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
	path('vendor/cart/remove/<int:cart_item>', views.cart_remove, name='cart-remove-vendor'),
	path('customer/cart/remove/<int:cart_item>', views.cart_remove, name='cart-remove-customer'),
	path('vendor/cart/update', views.cart_update, name='cart-update-vendor'),
	path('customer/cart/update', views.cart_update, name='cart-update-customer'),
	path('categories/<str:category>', views.category_details, name='category-details'),
	path('payment', views.payment, name='payment'),
	path('book/<int:book_id>', views.book_details, name='book-details'),

]