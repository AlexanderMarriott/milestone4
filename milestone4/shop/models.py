from django.db import models

from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=254, db_index=True)
    slug = models.SlugField(max_length=254, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list_category", args=[self.slug])


class Product(models.Model):

    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=254)
    brand = models.CharField(max_length=254, default="Un-branded")
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=254)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])
