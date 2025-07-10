from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class ItemDetails(models.Model):
    item_code = models.BigIntegerField(primary_key=True)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_desc = models.TextField()
    item_image = models.FileField(upload_to='image')
    item_category = models.CharField(max_length=255)

    def __str__(self):
        return self.item_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemDetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.item.item_name} ({self.quantity})"