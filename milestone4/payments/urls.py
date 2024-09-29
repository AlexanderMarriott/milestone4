from django.urls import path
from . import views

urlpatterns = [
    
    path("payment-success/", views.payment_success, name="payment-success"),

    path("payment-failed/", views.payment_failed, name="payment-failed"),

    path("checkout/", views.checkout, name="checkout"),

    path("complete-order/", views.complete_order_logic, name="complete-order"),

    path("create-checkout-session/", views.create_checkout_session, name="create-checkout-session"),

    path('webhook/', views.stripe_webhook, name='stripe_webhook'),



]




