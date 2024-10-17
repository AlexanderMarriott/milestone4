from decimal import Decimal
from shop.models import Product
from .models import Basket as BasketModel
from django.contrib.auth.models import User
import copy

class Basket:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        self.basket = self.get_basket()

    def get_basket(self):
        if self.user:
            basket_items = BasketModel.objects.filter(user=self.user)
            basket = {}
            for item in basket_items:
                basket[str(item.product.id)] = {
                    'price': str(item.product.price),
                    'quantity': item.quantity
                }
            return basket
        else:
            return self.session.get('basket', {})

    def add(self, product, quantity):
        if self.user:
            basket_item, created = BasketModel.objects.get_or_create(user=self.user, product=product)
            if not created:
                basket_item.quantity += quantity
            else:
                basket_item.quantity = quantity
            basket_item.save()
        else:
            product_id = str(product.id)
            if product_id not in self.basket:
                self.basket[product_id] = {'price': str(product.price), 'quantity': quantity}
            else:
                self.basket[product_id]['quantity'] += quantity
            self.session['basket'] = self.basket
            self.session.modified = True

    def update(self, product_id, quantity):
        if self.user:
            product = Product.objects.get(id=product_id)
            basket_item = BasketModel.objects.get(user=self.user, product=product)
            basket_item.quantity = quantity
            basket_item.save()
        else:
            product_id = str(product_id)
            if product_id in self.basket:
                self.basket[product_id]['quantity'] = quantity
                self.session.modified = True

    def delete(self, product_id):
        if self.user:
            product = Product.objects.get(id=product_id)
            BasketModel.objects.filter(user=self.user, product=product).delete()
        else:
            product_id = str(product_id)
            if product_id in self.basket:
                del self.basket[product_id]
                self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.basket.values())

    def __iter__(self):
        all_product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        basket = copy.deepcopy(self.basket)
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def clear(self):
        if self.user:
            BasketModel.objects.filter(user=self.user).delete()
        else:
            self.session['basket'] = {}
            self.session.modified = True
    

