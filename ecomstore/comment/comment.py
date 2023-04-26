from .models import Comment
from catalog.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect 
from .serializers import CommentResponseSerializer
import decimal # not needed yet but we will later
import random
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status


def get_product_comment(request):
    try:
        postdata = request.data
        product_slug = postdata.get('product_slug','')
        product_id = postdata.get('product_id', 0)
        if product_slug != '':
            return Comment.objects.filter(product_slug = product_slug)
        elif product_id != 0:
            return Comment.objects.filter(product_id = product_id)
        else:
            return []
    except Exception as e:
        return []


def create_comment(request):
    try:
        data = request.data
        product_id = data.get('product_id', 0)
        product = get_object_or_404(Product, id=product_id)
        content = data.get('content', "")
        rate = data.get('rate', 0)
        if rate < 1 or rate > 5 :
            raise Exception('Rate value must bettwen 1-5')
        if content == "" :
            raise Exception('Content must not be null')
        User = get_user_model()
        default_user = User.objects.first()
        comment = Comment.objects.create(
            product=product,
            user = default_user,
            content=content,
            rate = rate,
        )
        comment.save()
        return Response(CommentResponseSerializer(comment).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)