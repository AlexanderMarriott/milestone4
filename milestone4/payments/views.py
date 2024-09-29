from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from basket.basket import Basket
from django.http import JsonResponse
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    # Prefill the form with the user's saved info
    if request.user.is_authenticated:
        try:
            # Authenticated user WITH shipping info
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {
                "shipping": shipping_address,
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            }
            return render(request, "payments/checkout.html", context=context)
        except ShippingAddress.DoesNotExist:
            # Authenticated user WITHOUT shipping info
            context = {
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            }
            return render(request, "payments/checkout.html", context=context)
    else:
        context = {
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, "payments/checkout.html", context=context)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Fetch basket items for the user
            basket = Basket(request)
            total_cost = basket.get_total_price()

            # Create the order
            if request.user.is_authenticated:
                user = User.objects.get(id=request.user.id)
                order = Order.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    shipping_address=f"{data['address1']}, {data['address2']}, {data['city']}, {data['country']}, {data['postal_code']}",
                    amount_paid=total_cost,
                    user=user
                )
            else:
                order = Order.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    shipping_address=f"{data['address1']}, {data['address2']}, {data['city']}, {data['country']}, {data['postal_code']}",
                    amount_paid=total_cost
                )

            # Create order items
            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            # Prepare line items for Stripe
            line_items = []
            for item in basket:
                line_items.append({
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': item['product'].title,
                        },
                        'unit_amount': int(item['price'] * 100),  # Stripe expects amount in cents
                    },
                    'quantity': item['quantity'],
                })

            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=settings.DOMAIN_URL + '/payments/payment-success/',
                cancel_url=settings.DOMAIN_URL + '/payments/payment-failed/',
                metadata={
                    'order_id': order.id,
                }
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print("Invalid payload")
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print("Invalid signature")
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    print("Event type:", event['type'])
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("Checkout session completed:", session)
        complete_order_logic(session)

    return JsonResponse({'status': 'success'}, status=200)

def complete_order_logic(session):
    # Extract necessary information from the session metadata
    order_id = session['metadata']['order_id']
    order = Order.objects.get(id=order_id)
    order.payment_status = 'Completed'
    order.save()
    print("Order updated successfully")

def payment_success(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payments/payment-success.html')

def payment_failed(request): 
    return render(request, 'payments/payment-failed.html')
