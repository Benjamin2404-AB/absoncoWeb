import re
import uuid
from django.conf import settings
from django.db import models
from jupyterlab_server import slugify
# from jupyterlab_server import slugify

# Create your models here.
ITEM_TYPE_CHOICES = [
    ("Electricals", "Electricals"),
    ("Electronics", "Electronics"),
    ("Refrigeration", "Refrigeration"),
]

# Item Model
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discountprice = models.FloatField(blank=True,null=True)
    image = models.ImageField(upload_to="item_images/",default='a.jpg')
    itemType = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES)
    brand = models.CharField(max_length=100)

    slug =  models.SlugField(unique=True,blank=True,null=True)
            
       
    description = models.TextField(default="""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. """

                                   
                                   
                                   )
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from the title
        super().save(*args, **kwargs)
    
    



    def __str__(self) -> str:
        return self.title

class OrderItem(models.Model):
    item = models.ForeignKey(Item ,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title

#Shopping Cart
class Order(models.Model):
    
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    
    items = models.ManyToManyField(OrderItem)
    start_daate = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.title




