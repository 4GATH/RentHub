from django.contrib import admin

# Register your models here.
from .models import Category,product,Subcategory

admin.site.register(Category)
admin.site.register(product)
admin.site.register(Subcategory)
