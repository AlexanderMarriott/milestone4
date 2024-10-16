from django.contrib import admin
from .models import Basket

class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)

admin.site.register(Basket, BasketAdmin)
