from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from checkout.models import BaseOrderInfo

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        username = self.model.normalize_username(username)

        user = self.model(username=username, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractUser):

    first_name = None
    last_name = None

    email = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45, unique=True)
    date_of_birth = models.DateField(null=True)
    role = models.CharField(max_length=20, default="USER")
    telephoneNumber = models.CharField(max_length=20)
    deliveryAddress = models.CharField(max_length=200)
    verifyToken = models.CharField(max_length=200, default=None, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    

class UserProfile(BaseOrderInfo):
  # user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __unicode__(self):
    return 'User Profile for: ' + self.user.username
