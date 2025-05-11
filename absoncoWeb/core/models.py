from django.conf import settings
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField  

ITEM_TYPE_CHOICES = [
    ("Electricals", "Electricals"),
    ("Electronics", "Electronics"),
    ("Refrigeration", "Refrigeration"),
    ("Accessories", "Accessories"),
    ("General", "General"),
]
# core/models.py
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discountprice = models.FloatField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)  # Remove default
    itemType = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES)
    brand = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(default="""Lorem Ipsum is simply dummy text...""")
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
# class Item(models.Model):
#     title = models.CharField(max_length=100)
#     price = models.FloatField()
#     discountprice = models.FloatField(blank=True, null=True)
#     image = models.ImageField(upload_to="item_images/", default='a.jpg')
#     itemType = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES)
#     brand = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True, blank=True, null=True)
#     description = models.TextField(default="""Lorem Ipsum is simply dummy text...""")
#     time_added = models.DateTimeField(auto_now_add=True)
#     time_updated = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.title}"

    def get_total_price(self):
        return self.item.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateField(null=True, blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.user.username} (Ordered: {self.ordered})"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())