from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Payment)