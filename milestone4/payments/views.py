from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from basket.basket import Basket
from django.http import JsonResponse
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
import json

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

def complete_order_logic(session):
    # Extract necessary information from the session metadata
    first_name = session['metadata']['first_name']
    last_name = session['metadata']['last_name']
    email = session['metadata']['email']
    address1 = session['metadata']['address1']
    address2 = session['metadata']['address2']
    city = session['metadata']['city']
    country = session['metadata']['country']
    postal_code = session['metadata']['postal_code']

    # Create the order
    basket = Basket(session)
    total_cost = basket.get_total_price()

    if session['metadata']['user_id']:
        user = User.objects.get(id=session['metadata']['user_id'])
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            shipping_address=f"{address1}, {address2}, {city}, {country}, {postal_code}",
            amount_paid=total_cost,
            user=user
        )
    else:
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            shipping_address=f"{address1}, {address2}, {city}, {country}, {postal_code}",
            amount_paid=total_cost
        )

    for item in basket:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price']
        )

    basket.clear()

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # Set this in your settings

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        complete_order_logic(session)  # Call your function to handle order completion

    return JsonResponse({'status': 'success'}, status=200)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'T-shirt',
                            },
                            'unit_amount': 2000,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.DOMAIN_URL + '/payment-success/',
                cancel_url=settings.DOMAIN_URL + '/payment-failed/',
                metadata={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'address1': data['address1'],
                    'address2': data['address2'],
                    'city': data['city'],
                    'country': data['country'],
                    'postal_code': data['postal_code'],
                    'user_id': request.user.id if request.user.is_authenticated else None,
                }
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_success(request):
    return render(request, 'payments/payment-success.html')

def payment_failed(request): 
    return render(request, 'payments/payment-failed.html')

