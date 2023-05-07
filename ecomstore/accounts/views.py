
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignUpSerializer, UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .jwtToken import create_jwt_pair_for_user

from accounts.models import User
from django.shortcuts import get_object_or_404

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings

from django.contrib.auth.hashers import check_password


creds = credentials.Certificate(settings.FIREBASE_CONFIG)
firebase_app = firebase_admin.initialize_app(creds)

# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def UserRegister(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password'])
        serializer.save()

        return Response({
            'success': True,
            'code': 201,
            'message': 'Register successful!',
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    else:
        return Response({
            'success': False,
            'code': 400,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def UserRegisterWithGoogleAndGoogle(request):
    try:
        auth_header = request.data.get('token')
        token = auth_header
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['user_id']
        try:
            user = get_object_or_404(User, verifyToken=user_id)

            # đăng nhập
            if user:
                user_verify = authenticate(
                    request,
                    username=decoded_token['email'],
                    password=user_id
                )

                if user_verify:
                    tokens = create_jwt_pair_for_user(user_verify)
                    data = {
                        'success': True,
                        'code': 200,
                        "message": "Login Successfull",
                        "tokens": tokens}

                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'success': False,
                        'code': 400,
                        'message': 'Username or password is incorrect!',
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # đăng ki
            data = {
                "name": decoded_token.get("name", ""),
                "username": decoded_token.get("email", ""),
                "email": decoded_token.get("email", ""),
                "password": user_id,
                "verifyToken": user_id
            }
            serializer = SignUpSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(
                    serializer.validated_data['password'])
                serializer.save()
                # đăng nhập sau khi đã đăng kí

                user = get_object_or_404(User, verifyToken=user_id)
                if user:
                    user_verify = authenticate(
                        request,
                        username=decoded_token['email'],
                        password=user_id
                    )

                    if user_verify:
                        tokens = create_jwt_pair_for_user(user_verify)
                        data = {
                            'success': True,
                            'code': 200,
                            "message": "Login Successfull",
                            "tokens": tokens}

                        return Response(data, status=status.HTTP_200_OK)
                return Response({
                    'success': False,
                    'code': 400,
                    'message': 'Username or password is incorrect!',
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'success': False,
                'code': 400,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'error_message': str(e),
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def UserLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(
        request,
        username=username,
        password=password
    )
    if user:
        tokens = create_jwt_pair_for_user(user)
        data = {
            'success': True,
            'code': 200,
            "message": "Login Successfull",
            "tokens": tokens}
        return Response(data, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'code': 400,
        'message': 'Username or password is incorrect!',
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user, many=False)

        return Response({
            'success': True,
            'code': 200,
            "message": "Get Profile Successfull",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error_message': str(e),
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, id=user_id)

        if not (request.data.get('name') or request.data.get('email') or request.data.get('username') or request.data.get('telephoneNumber') or request.data.get('deliveryAddress')):
            return Response({
                'success': False,
                'code': 400,
                'message': "All Fields cannot be empty",
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('email'):
            user.email = request.data.get('email')
        if request.data.get('username'):
            user.username = request.data.get('username')
        if request.data.get('telephoneNumber'):
            user.telephoneNumber = request.data.get('telephoneNumber')
        if request.data.get('deliveryAddress'):
            user.deliveryAddress = request.data.get('deliveryAddress')
        if request.data.get('name'):
            user.name = request.data.get('name')
        user.save()

        return Response({
            'success': True,
            'code': 200,
            "message": "Update Successful"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error_message': str(e),
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, id=user_id)

        if not (request.data.get('oldPassword') and request.data.get('newPassword')):
            return Response({
                'success': False,
                'code': 400,
                'message': "oldPassword field and newPassword field cannot be empty",
            }, status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get('oldPassword') == request.data.get('newPassword')):
            return Response({
                'success': False,
                'code': 400,
                'message': "oldPassword field and newPassword must be different",
            }, status=status.HTTP_400_BAD_REQUEST)
        if user.verifyToken:
            return Response({
                'success': False,
                'code': 400,
                'message': "Unable to change the password of account supply by google and facebook",
            }, status=status.HTTP_400_BAD_REQUEST)
        print(user.verifyToken)

        if check_password(request.data.get('oldPassword'), user.password):
            user.password = make_password(request.data.get('newPassword'))
            user.save()
            return Response({
                'success': True,
                'code': 200,
                "message": "Change Password Successful"
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'code': 400,
            "message": "Password is wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error_message': str(e),
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'success': True,
                         'code': 200, 'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False,
                         'code': 400, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
