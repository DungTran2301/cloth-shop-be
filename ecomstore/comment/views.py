from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentResponseSerializer
from rest_framework.decorators import api_view
from . import comment

@api_view(['POST'])
def create_comment(request):
    if request.method == 'POST':
        return comment.create_comment(request)
    print('hello')

@api_view(['POST']) 
def get_product_comment(request):
    if request.method == 'POST':
        try:
            comments = comment.get_product_comment(request)
            serializers = CommentResponseSerializer(comments, many=True)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)