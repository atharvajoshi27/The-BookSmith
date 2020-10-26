from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import os
# from PIL import Image
from BookSmith.settings import BASE_DIR
# import regex

# Create your models here.

def validate_contact_number(contact_number):
	if not (1000000000 <= contact_number <= 9999999999):
		raise ValidationError('Contact number must ne a 10 digit number')
	else:
		return contact_number


class User(AbstractUser, models.Model):
	user_id = models.AutoField(primary_key=True)
	contact_number = models.IntegerField(validators=[validate_contact_number])
	address = models.TextField()
	REQUIRED_FIELDS = ['contact_number', 'address']


class Customer(models.Model):
	customer_id = models.AutoField(primary_key=True)
	customer_details = models.ForeignKey(User, on_delete=models.CASCADE)



class Vendor(models.Model):
	vendor_id = models.AutoField(primary_key=True)
	vendor_details = models.ForeignKey(User, on_delete=models.CASCADE)



class Category(models.Model):
	category_id = models.AutoField(primary_key=True)        
	category = models.CharField(max_length=25)



class Book(models.Model):
	book_id = models.AutoField(primary_key=True)
	book_name = models.CharField(max_length=50)
	book_edition = models.DecimalField(max_digits=6, decimal_places=2)
	book_price = models.DecimalField(max_digits=6, decimal_places=2)
	book_quantity = models.IntegerField()
	is_new = models.BooleanField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
		

class CartItem(models.Model):
	cartitem_id = models.AutoField(primary_key=True)
	# total_price = models.DecimalField(max_digits=6, decimal_place=2)
	book_quantity = models.IntegerField()
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)


class Cart(models.Model):
	cart_id = models.AutoField(primary_key=True)
	customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Payment(models.Model):
	payment_choices = (
		('CC', 'Credit Card'),
		('DC', 'Debit Card'),
		('NB', 'Net Banking'),
		('GP', 'Google Pay'),
	)
	payment_id = models.AutoField(primary_key=True)
	payment_type = models.CharField(max_length=4, choices=payment_choices)
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	payment_date = models.DateTimeField(auto_now_add=True)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)