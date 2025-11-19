"""
URL configuration for rntsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from home.views import *
from home import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homefn),
    path('dashboard/',homefn),
    path('viewproduct/<int:p_id>/', views.viewproductfn, name='viewproduct'),
    path('carview',carviewfn),
    path('bikeview',bikeviewfn),
    path('brandsview/', views.all_brandsfn,),
    path('brand/<int:id>/', views.brand_vehicles, name='brand_vehicles'),
    path('addproduct/',add_productfn,),
    path('allproducts/', views.add_productfn, name='all_products'),
    path('add_rental/<int:id>/', add_rentalfn, name='add_rental'),
    path('add_rental/', views.add_rental_page, name='add_rental_page'),
    path('rentals/', rental_listfn, name='rental_list'),
    path('edit_rental/<int:id>/', views.edit_rentalfn, name='edit_rental'),
    path('delete_rental/<int:id>/', views.delete_rentalfn, name='delete_rental'),
    path('login/', views.loginfn, name='login'),
    path('logout/', views.logoutfn, name='logout')


    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)