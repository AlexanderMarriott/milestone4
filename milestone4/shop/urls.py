from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # main page
    path("", views.store, name="shop"),
    # product detail page
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    # category page
    path("search/<slug:category_slug>/", views.list_category, name="list_category"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
