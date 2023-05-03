from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import UserRegister, UserLogin, get_user_profile, update_user_profile, logout

urlpatterns = [
    path('auth/signup/', UserRegister, name="register"),
    path('auth/login/', UserLogin, name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout, name="logout"),
    path('profile/', get_user_profile, name="get_user_profile"),
    path('update/', update_user_profile, name="update_user_profile"),

]
