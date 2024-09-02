from django.urls import path

from . import views

urlpatterns = [
    path("", views.store, name="shop"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]
