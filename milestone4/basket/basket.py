class basket:

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
