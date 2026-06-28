from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render

from .models import Customer, Product, Quote
from .forms import CustomerForm, ProductForm, QuoteForm, QuoteItemFormSet


# Create your views here.

def home(request):
    context = {
        'customer_count': Customer.objects.count(),
        'product_count': Product.objects.count(),
        'quote_count': Quote.objects.count(),
    }
    return render(request, 'home.html', context)

def quote_list(request):
    quotes = Quote.objects.select_related('customer').order_by('-date_created')
    return render(request, 'quote_list.html', {'quotes': quotes})

def create_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        item_formset = QuoteItemFormSet(request.POST)
        if form.is_valid() and item_formset.is_valid():
            quote = form.save(commit=False)
            quote.subtotal = Decimal('0.00')
            quote.total = quote.delivery_cost
            quote.save()

            item_formset.instance = quote
            item_formset.save()
            update_quote_totals(quote)
            return redirect('quote_detail', pk=quote.pk)
    else:
        form = QuoteForm()
        item_formset = QuoteItemFormSet()

    return render(request, 'create_quote.html', {
        'form': form,
        'item_formset': item_formset,
    })

def quote_detail(request, pk):
    quote = get_object_or_404(
        Quote.objects.select_related('customer').prefetch_related('items__product'),
        pk=pk,
    )
    return render(request, 'quote_detail.html', {'quote': quote})

def edit_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        item_formset = QuoteItemFormSet(request.POST, instance=quote)
        if form.is_valid() and item_formset.is_valid():
            quote = form.save()
            item_formset.save()
            update_quote_totals(quote)
            return redirect('quote_detail', pk=quote.pk)
    else:
        form = QuoteForm(instance=quote)
        item_formset = QuoteItemFormSet(instance=quote)

    return render(request, 'create_quote.html', {
        'form': form,
        'item_formset': item_formset,
        'quote': quote,
    })

def delete_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)

    if request.method == 'POST':
        quote.delete()
        return redirect('quote_list')

    return render(request, 'delete_quote.html', {'quote': quote})

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_quote')
    else:
        form = CustomerForm()

    return render(request, 'create_customer.html', {'form': form})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_quote')
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})

def generate_pdf(request, pk):
    quote = get_object_or_404(Quote.objects.select_related('customer'), pk=pk)
    return render(request, 'quote_detail.html', {'quote': quote})

update_quote = edit_quote


def update_quote_totals(quote):
    subtotal = sum((item.item_total for item in quote.items.all()), Decimal('0.00'))
    quote.subtotal = subtotal
    quote.total = subtotal + quote.delivery_cost
    quote.save(update_fields=['subtotal', 'total'])
