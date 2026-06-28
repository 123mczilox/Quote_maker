from django.contrib import admin

from .models import Customer, Product, Quote, QuoteItem


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Quote)
admin.site.register(QuoteItem)
