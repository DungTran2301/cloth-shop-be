from django.db import models
from django.urls import reverse
from django.core.validators import DecimalValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(max_length=50, unique=True,
  help_text='Unique value for product page URL, created from name.')
  description = models.TextField()
  is_active = models.BooleanField(default=True)
  meta_keywords = models.CharField("Meta Keywords", max_length=255,
                                  help_text='Comma-delimited set of SEO keywords for meta tag')
  meta_description = models.CharField("Meta Description", max_length=255,
  help_text='Content for description meta tag')
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
  BOOK_COVER_CHOICES = (  # new
    ("BIA_CUNG", "Bìa cứng"),
    ("BIA_MEM", "Bìa mềm")
  )
  
  name = models.CharField(max_length=255, unique=True)
  slug = models.SlugField(max_length=255, unique=True,
  help_text='Unique value for product page URL, created from name.')



  supplier = models.CharField(max_length=255, default="null")
  publisher = models.CharField(max_length=255, default="null")
  author = models.CharField(max_length=255, default="null")
  book_cover = models.CharField(
    choices = BOOK_COVER_CHOICES,
    max_length = 100,
    verbose_name="Status of the category",
    default='Bìa mềm'
  )

  sku = models.CharField(max_length=50)
  price = models.DecimalField(max_digits=9,decimal_places=2)
  old_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True,default=0.00)
  discount = models.DecimalField(max_digits=9,
                                 decimal_places=2, 
                                 blank=True,default=0.00,
                                 validators=[MinValueValidator(0), MaxValueValidator(1)])

  image = models.ImageField(upload_to='static/images/products/main', default='')
  thumbnail = models.ImageField(upload_to='static/images/products/thumbnails', default='')
  image_caption = models.CharField(max_length=200,default='')

  is_active = models.BooleanField(default=True)
  is_bestseller = models.BooleanField(default=False)
  is_featured = models.BooleanField(default=False)
  quantity = models.IntegerField()
  description = models.TextField()
  meta_keywords = models.CharField(max_length=255,
  help_text='Comma-delimited set of SEO keywords for meta tag')
  meta_description = models.CharField(max_length=255,
  help_text='Content for description meta tag')
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
