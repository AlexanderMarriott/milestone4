from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from basket.basket import Basket
from django.http import JsonResponse
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt

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

def complete_order(request):
    if request.POST.get('action') == 'post':
        # Get the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')

        # Create the order
        basket = Basket(request)
        total_cost = basket.get_total_price()

        if request.user.is_authenticated:
            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                shipping_address=f"{address1}, {address2}, {city}, {country}, {postal_code}",
                amount_paid=total_cost,
                user=request.user
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
        return JsonResponse({'success': True})

def create_checkout_session(request):
    if request.method == 'POST':
        try:
            basket = Basket(request)
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

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri('/payments/payment-success/'),
                cancel_url=request.build_absolute_uri('/payments/payment-failed/'),
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
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
        complete_order(session)  # Call your function to handle order completion

    return JsonResponse({'status': 'success'}, status=200)

def payment_success(request):
    return render(request, 'payments/payment-success.html')

def payment_failed(request): 
    return render(request, 'payments/payment-failed.html')

