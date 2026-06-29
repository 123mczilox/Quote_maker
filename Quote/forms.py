from django import forms
from django.forms import inlineformset_factory

from .models import Customer, Product, Quote, QuoteItem

class QuoteForm(forms.ModelForm):
    valid_until = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = Quote
        fields = [
            'quote_number',
            'customer',
            'valid_until',
            'delivery_cost',
            'notes',
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'email',
            'phone_number',
            'address'
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'color',
            'gauge',
            'description',
        ]


QuoteItemFormSet = inlineformset_factory(
    Quote,
    QuoteItem,
    fields=[
        'product',
        'description',
        'color',
        'gauge',
        'quantity',
        'length',
        'unit_price',
    ],
    extra=3,
    can_delete=True,
)
