from django.shortcuts import render


def payment_success(request):
    return render(request, "payments/payment-success.html")

def payment_failed(request):
    return render(request, "payments/payment-failed.html")
