from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from catalog.models import Product
# Create your models here.

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=5,
                                 validators=[MinValueValidator(0), MaxValueValidator(1)])
    def __str__(self):
        return f'{self.user.username}\'s comment on {self.product.name}'