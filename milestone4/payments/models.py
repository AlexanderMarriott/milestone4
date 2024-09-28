from django.db import models

from django.contrib.auth.models import User

from shop.models import Product

class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=12)
    country = models.CharField(max_length=50)

    #foreign key to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'


    def __str__(self):
        if self.user:
            return 'Shipping Address for {}'.format(self.user.username)
        else:

            return 'Shipping Address for an anonymous user'

# Create your models here.

class Order(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    #foreign key to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        
        return 'order - #' + str(self.id)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
        #foreign key to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order Item for order #' + str(self.order.id) + ' - ' + self.product.title

