from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import  *
from .forms import ProductForm,RentalForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone




def homefn(request):
    x= product.objects.all()
    return render (request,'home.html',{'xyz':x})

def viewproductfn(request,p_id):
    x= product.objects.get(id=p_id)
    return render (request,'product.html',{'abc':x})


def carviewfn(request):

    car_category = get_object_or_404(Category, name__iexact='Car')
    car_brands = car_category.subcategories.all()
    car_products = product.objects.filter(subcategory__category=car_category,is_available=True )

    return render(request, 'carview.html', {
        'car_category': car_category,
        'car_brands': car_brands,
        'car_products': car_products,
    })


def bikeviewfn(request):
    bike_category =get_object_or_404(Category,name__iexact='Bike')
    bike_brands = bike_category.subcategories.all()
    bike_products= product.objects.filter(subcategory__category=bike_category, is_available=True)

    return render(request,'bikeview.html', {
        'bike_category':bike_category,
        'bike_brands': bike_brands,
        'bike_products':bike_products
    })


def all_brandsfn(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'brands.html', {
        'categories': categories
    })

def brand_vehicles(request, id):
    brand = get_object_or_404(Subcategory, id=id)
    vehicles = product.objects.filter(subcategory=brand).order_by('name')

    return render(request, 'brand_vehicles.html', {
        'brand': brand,
        'vehicles': vehicles,
    })



def add_productfn(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            subcategory = form.cleaned_data.get('subcategory')
            new_category_name = form.cleaned_data.get('new_category_name')
            new_brand_name = form.cleaned_data.get('new_brand_name')
            new_brand_logo = form.cleaned_data.get('new_brand_logo')

            # ✅ If user added a new category, create or get it
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)

            # ✅ If user added a new brand (subcategory), create it under the selected or new category
            if new_brand_name and category:
                subcategory = Subcategory.objects.create(
                    category=category,
                    brand_name=new_brand_name,
                    logo=new_brand_logo
                )

            # ✅ Create the product
            new_product = form.save(commit=False)
            new_product.subcategory = subcategory
            new_product.is_available = True  # ensure product is available for renting
            new_product.save()

            messages.success(request, "✅ Product added successfully!")
            return redirect('all_products')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})





def add_rentalfn(request, id):
    product_instance = get_object_or_404(product, id=id)

    
    if not product_instance.is_available:
        messages.error(request, f"{product_instance.name} is already rented!")
        return redirect('rental_list')

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.product = product_instance
            rental.status = 'Active'
            rental.save()

            # Mark product as unavailable
            product_instance.is_available = False
            product_instance.save()

            messages.success(request, f"{product_instance.name} rented successfully!")
            return redirect('rental_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RentalForm(initial={'product': product_instance})

        # ✅ Make sure dropdown only shows available vehicles + current one
        available_products = product.objects.filter(is_available=True) | product.objects.filter(id=product_instance.id)
        form.fields['product'].queryset = available_products.distinct()

    return render(request, 'add_rental.html', {
        'form': form,
        'product': product_instance
    })


# 🔹 Add rental manually (from "Add New Rental" page)
def add_rental_page(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.status = 'Active'
            rental.save()

            # Mark the rented vehicle as unavailable
            rented_product = rental.product
            rented_product.is_available = False
            rented_product.save()

            messages.success(request, f"{rented_product.name} rented successfully!")
            return redirect('rental_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RentalForm()

        # ✅ Only show available vehicles in dropdown
        form.fields['product'].queryset = product.objects.filter(is_available=True)

    return render(request, 'add_rental.html', {'form': form})


def rental_listfn(request):

    auto_return_expired_rentals()

    rentals = Rental.objects.all().order_by('-created_at')
    return render(request, 'rental_list.html', {'rentals': rentals})


def edit_rentalfn(request, id):
    rental = get_object_or_404(Rental, id=id)

    if request.method == 'POST':
        form = RentalForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            messages.success(request, "Rental updated successfully!")
            return redirect('rental_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RentalForm(instance=rental)

        # ✅ Show only available vehicles + the one currently rented in this record
        available_products = product.objects.filter(is_available=True) | product.objects.filter(id=rental.product.id)
        form.fields['product'].queryset = available_products.distinct()

    return render(request, 'add_rental.html', {
        'form': form,
        'edit_mode': True
    })

def delete_rentalfn(request, id):
    try:
        rental = Rental.objects.get(id=id)
        product = rental.product
        product.is_available = True
        product.save()
        rental.delete()
        messages.success(request, "Rental deleted successfully!")
    except Rental.DoesNotExist:
        messages.warning(request, "This rental no longer exists.")

    return redirect('rental_list')




def complete_rental(rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.status = 'Completed'
    rental.save()

    rental.product.is_available = True
    rental.product.save()


def auto_return_expired_rentals():
    today = timezone.now().date()

    expired_rentals = Rental.objects.filter(
        end_date__lt=today,
        status='Active'
    )

    for rental in expired_rentals:
        rental.status = 'Completed'
        rental.save()

        # make vehicle available again
        rental.product.is_available = True
        rental.product.save()



def loginfn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('/')  # change this to your main page name
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

# 🔹 Logout Function
@login_required
def logoutfn(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

