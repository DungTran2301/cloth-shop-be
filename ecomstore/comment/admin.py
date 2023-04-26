from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'content', 'rate', 'created_at') # Customize the fields displayed in the admin list view
    list_filter = ('product', 'user', 'created_at') # Add filtering options for the product, user, and created_at fields
    search_fields = ('product__name', 'user__username') # Add search functionality for the related Product name and User username fields

admin.site.register(Comment, CommentAdmin)