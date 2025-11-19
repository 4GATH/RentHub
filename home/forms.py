from django import forms
from .models import product, Subcategory, Category,Rental
from django import forms

from django import forms
from .models import product, Category, Subcategory

class ProductForm(forms.ModelForm):
    # Optional fields for creating new Category or Brand (Subcategory)
    new_category_name = forms.CharField(
        max_length=50,
        required=False,
        label="Or Add New Category",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new category name'
        })
    )

    new_brand_name = forms.CharField(
        max_length=50,
        required=False,
        label="Or Add New Brand",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new brand name'
        })
    )

    new_brand_logo = forms.ImageField(
        required=False,
        label="Brand Logo",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    # Existing dropdowns
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Select Existing Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        label="Select Existing Brand",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = product
        fields = [
            'category',
            'subcategory',
            'name',
            'price',
            'image',
            'description',
            'is_available',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter vehicle name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter short description'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Optional improvement: only show available subcategories
        self.fields['subcategory'].queryset = Subcategory.objects.all()



    class Meta:
        model = product   # if your model class name is 'product' (lowercase)
        fields = ['category', 'subcategory', 'name', 'description','price', 'image']
        widgets = {
                    'description': forms.Textarea(attrs={
                    'class': 'form-control my-description',  # Add your custom CSS classes
                    'placeholder': 'Enter product details...',
                    'rows': 4,
                     'style': 'resize:none;'  # Inline CSS example
            }),
        }
        






class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = [
            'product',
            'renter_name',
            'renter_contact',
            'start_date',
            'end_date',
            'total_price'
        ]
        widgets = {
            'renter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer name'}),
            'renter_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total amount'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].queryset = product.objects.filter(is_available=True)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})