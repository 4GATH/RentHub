from django.db import models
from django.utils import timezone
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey( Category, on_delete=models.CASCADE,  related_name='subcategories')
    brand_name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='logo_pic', blank=True, null=True)

    def __str__(self):
        return self.brand_name




class product(models.Model):
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='pro_pic', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    


class Rental(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    renter_name = models.CharField(max_length=100)
    renter_contact = models.CharField(max_length=15, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Completed', 'Completed'),
        ],
        default='Active'
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} rented to {self.renter_name}"

    def duration(self):
        return (self.end_date - self.start_date).days




