from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('customers/create/', views.create_customer, name='create_customer'),
    path('products/create/', views.create_product, name='create_product'),

    path('quotes/', views.quote_list, name='quote_list'),

    path('quotes/new/', views.create_quote, name='create_quote'),
    path('quotes/create/', views.create_quote, name='create_quote_alt'),

    path('quotes/<int:pk>/', views.quote_detail, name='quote_detail'),

    path('quotes/<int:pk>/edit/', views.edit_quote, name='edit_quote'),
    path('quotes/<int:pk>/edit/', views.edit_quote, name='update_quote'),
    path('quotes/<int:pk>/delete/', views.delete_quote, name='delete_quote'),

    path('quotes/<int:pk>/pdf/', views.generate_pdf, name='generate_pdf'),
]
