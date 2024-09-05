from django.shortcuts import render


def basket_summary(request):
    return render(request, "basket/basket_summary.html")


def basket_add(request):
    pass


def basket_delete(request):
    pass


def basket_update(request):
    pass
