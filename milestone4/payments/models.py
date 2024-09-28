from django.db import models

from django.contrib.auth.models import User

from django.db import models

from django.utils import timezone

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
        return 'Shipping Address for an anonymous user'

# Create your models here.
