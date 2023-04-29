from django.db import models
from django.urls import reverse
from django.core.validators import DecimalValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'categories'
    ordering = ['-created_at']
    verbose_name_plural = 'Categories'

  def __unicode__(self):
    return self.name
  def get_absolute_url(self):
    return reverse('catalog_category', args={ self.slug })
  
class Product(models.Model):
  name = models.CharField(max_length=255, unique=True)
  supplier = models.CharField(max_length=255, default="null")
  sku = models.CharField(max_length=50)
  price = models.DecimalField(max_digits=9,decimal_places=2)
  old_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True,default=0.00)
  discount = models.DecimalField(max_digits=9,
                                 decimal_places=2, 
                                 blank=True,default=0.00,
                                 validators=[MinValueValidator(0), MaxValueValidator(1)])

  image = models.CharField(max_length=255, default=None)

  quantity = models.IntegerField()
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  categories = models.ManyToManyField(Category)

  class Meta:
    db_table = 'products'
    ordering = ['-created_at'] 
  def __unicode__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('catalog_product', args={ self.slug })
  def sale_price(self):
    if self.old_price > self.price:
      return self.price
    else:
      return None
