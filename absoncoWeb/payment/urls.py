# payment/urls.py
from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='success'),  # Handles Paystack callback
    path('success-clean/', views.payment_success_clean, name='success_clean'),  # Clean success page
    path('cancel/', views.payment_cancel, name='cancel'),
    path('paystack-webhook/', views.paystack_webhook, name='paystack_webhook'),
]