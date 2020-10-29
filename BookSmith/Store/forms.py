from django.forms import ModelForm, Textarea
from django import forms
from .models import User, Book


class CreateUser(ModelForm):
	class Meta:
		# print(User.__dict__)
		model = User
		fields = ['first_name', 'last_name', 'contact_number', 'address', 'is_vendor', 'username', 'email', 'password', ]
	
	# def __init__(self, *args, **kwargs):
	# 	super(CreateUser, self).__init__(*args, **kwargs)

class AddBook(ModelForm):
	class Meta:
		model = Book
		fields = ['book_name', 'book_edition', 'book_price', 'book_quantity', 'is_new', 'image_file', 'book_author', ]