# payment/views.py
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from django.utils import timezone
import requests
from core.models import Order
from django.contrib import messages

@login_required
def checkout_view(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if not order or not order.items.exists():
        messages.warning(request, "Your cart is empty.")
        return render(request, 'payment/checkout.html', {
            'order': None,
            'error': 'Your cart is empty.',
            'cart_total': 0
        })

    # Calculate cart total manually
    cart_total = sum(item.get_total_price() for item in order.items.all())

    if cart_total == 0:
        messages.warning(request, "Your cart total is zero. Please check your items.")

    return render(request, 'payment/checkout.html', {
        'order': order,
        'cart_total': cart_total
    })

@login_required
@csrf_protect
def create_checkout_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        order = Order.objects.filter(user=request.user, ordered=False).first()
        if not order or not order.items.exists():
            return JsonResponse({'error': 'No active order found or cart is empty'}, status=400)

        # Calculate total
        cart_total = sum(item.get_total_price() for item in order.items.all())
        if cart_total <= 0:
            return JsonResponse({'error': 'Cart total is zero'}, status=400)

        # Initialize Paystack transaction
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': request.user.email,
            'amount': int(cart_total * 100),  # Convert GHS to pesewas
            'currency': 'GHS',
            'reference': f'order_{order.id}_{int(timezone.now().timestamp())}',
            'callback_url': settings.PAYMENT_SUCCESS_URL,
            'cancel_url': settings.PAYMENT_CANCEL_URL,  # Added cancel_url
            'metadata': {
                'order_id': str(order.id),
                'user_id': str(request.user.id),
            },
            'channels': ['card', 'mobile_money', 'bank'],
        }
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            headers=headers,
            json=data
        )
        response_data = response.json()

        if response.status_code == 200 and response_data.get('status'):
            return JsonResponse({
                'authorization_url': response_data['data']['authorization_url'],
                'reference': response_data['data']['reference']
            })
        else:
            return JsonResponse({'error': response_data.get('message', 'Failed to initialize payment')}, status=400)

    except requests.RequestException as e:
        return JsonResponse({'error': f'Payment error: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@login_required
def payment_success(request):
    reference = request.GET.get('reference') or request.GET.get('trxref')

    if reference:
        try:
            # Verify transaction with Paystack
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            }
            response = requests.get(
                f'https://api.paystack.co/transaction/verify/{reference}',
                headers=headers
            )
            response_data = response.json()

            if response.status_code == 200 and response_data.get('status') and response_data['data']['status'] == 'success':
                order_id = response_data['data']['metadata']['order_id']
                order = Order.objects.get(id=order_id, user=request.user, ordered=False)
                order.ordered = True
                order.ordered_date = timezone.now()
                order.save()
                messages.success(request, f"Payment successful! Your order #{order.id} has been processed.")
            else:
                messages.error(request, "Payment verification failed. Please contact support.")
        except (requests.RequestException, Order.DoesNotExist, KeyError) as e:
            messages.error(request, "Error processing payment. Please contact support.")
    else:
        messages.warning(request, "No payment reference provided. Please try again or contact support.")

    # Always redirect to clean URL
    return redirect('payment:success_clean')

@csrf_exempt
def payment_success_clean(request):
    return render(request, 'payment/success.html')

@login_required
def payment_cancel(request):
    messages.warning(request, "Payment was cancelled.")
    return render(request, 'payment/cancel.html')

@csrf_exempt
def paystack_webhook(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    payload = request.body.decode('utf-8')
    import json
    try:
        event = json.loads(payload)
        if event['event'] == 'charge.success':
            reference = event['data']['reference']
            order_id = event['data']['metadata']['order_id']
            order = Order.objects.get(id=order_id, ordered=False)
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        return HttpResponse(status=200)
    except (ValueError, KeyError, Order.DoesNotExist) as e:
        return HttpResponse(status=400)