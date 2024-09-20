from decimal import Decimal

from shop.models import Product


class Basket:

    def __init__(self, request):

        self.session = request.session

        # Check if the session key exists
        basket = self.session.get("sKey")
        # If the session key does not exist, create a new session key
        if "sKey" not in request.session:
            basket = request.session["sKey"] = {}

        self.basket = basket

    def add(self, product, quantity):
        product_id = product.id

        # If the product is not in the basket, add it
        if product_id not in self.basket:
            self.basket[product_id] = {
                "price": str(product.price),
                "quantity": quantity,
            }

        # If the product is in the basket, update the quantity
        else:
            self.basket[product_id]["quantity"] = quantity

        self.session.modified = True





    def delete(self, product):
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.session.modified = True


    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = quantity
        if product_id in self.basket:
            self.basket[product_id]["quantity"] = product_quantity
            self.session.modified = True

    def __len__(self):
        return sum(item["quantity"] for item in self.basket.values())

    def __iter__(self):

        all_product_ids = self.basket.keys()

        products = Product.objects.filter(id__in=all_product_ids)

        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.basket.values()
        )

