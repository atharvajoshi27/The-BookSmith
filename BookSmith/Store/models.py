from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import os
from PIL import Image
from BookSmith.settings import BASE_DIR
# import regex

# Create your models here.

UPLOAD_TO = "images/"

def validate_contact_number(contact_number):
	if not (1000000000 <= contact_number <= 9999999999):
		raise ValidationError('Contact number must ne a 10 digit number')
	else:
		return contact_number


class User(AbstractUser):
	vendor_choice = (
		(1 , 'Yes'),
		(0 , 'No'),
	)
	user_id = models.AutoField(primary_key=True)
	contact_number = models.IntegerField(validators=[validate_contact_number])
	address = models.TextField()
	is_vendor = models.BooleanField(choices=vendor_choice)
	REQUIRED_FIELDS = ['contact_number', 'address', 'is_vendor']


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
	old_new = (
		(1, 'Yes'),
		(0, 'No'),
	)
	book_id = models.AutoField(primary_key=True)
	book_name = models.CharField(max_length=50)
	book_author = models.CharField(max_length=50)
	book_edition = models.DecimalField(max_digits=6, decimal_places=1)
	book_price = models.DecimalField(max_digits=6, decimal_places=2)
	book_quantity = models.IntegerField()
	date = models.DateTimeField(auto_now=True)
	is_new = models.BooleanField(choices=old_new)
	image_file = models.ImageField(upload_to=UPLOAD_TO)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		super(Book, self).save(*args, **kwargs)
		filename = self.image_file.name
		_, extension = filename.split('.')
		new_name = f"{UPLOAD_TO}image_{self.book_id}.{extension}"
		location = r"{BASE_DIR}/media/".format(BASE_DIR=BASE_DIR)
		os.rename(r"{location}/{filename}".format(location=location,filename=filename), r"{location}/{new_name}".format(location=location, new_name=new_name))
		self.image_file.name = new_name
		print("Path = ", self.image_file.path)
		print("url = ", self.image_file.url)
		print("filename = ", self.image_file.name)
		super(Book, self).save(*args, **kwargs)

		filename = self.image_file.path
		im = Image.open(filename)
		print(im.size)
		im = im.resize((700, 700), Image.ANTIALIAS)
		print(im.size)
		quality_val = 100
		im.save(filename, quality=quality_val)
		
class Cart(models.Model):
	cart_id = models.AutoField(primary_key=True)
	customer_id = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
	cartitem_id = models.AutoField(primary_key=True)
	# total_price = models.DecimalField(max_digits=6, decimal_place=2)
	book_quantity = models.IntegerField(default=0)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)



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
	# cart = models.ForeignKey(rCart, on_delete=models.CASCADE)
	customer_id = models.ForeignKey(User, on_delete=models.CASCADE)