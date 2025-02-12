from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Hash the password
        self.save()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class Spam(models.Model):
    phone_number = models.CharField(max_length=10, unique=True)
    is_spam = models.BooleanField(default=True)

    def __str__(self):
        return self.phone_number




