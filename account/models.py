from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.password_validation import validate_password


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password, is_seller=False, national_code=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number must be set')
        if not password:
            raise ValueError('Password must be set')

        if is_seller and not national_code:
            raise ValueError('National code is required for sellers')

        user = self.model(
            phone=phone,
            is_seller=is_seller,
            national_code=national_code if is_seller else None,
            **extra_fields
        )
        validate_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, is_seller=False, national_code=None, **extra_fields):
        return self._create_user(phone, password, is_seller, national_code, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        return self._create_user(phone, password, is_staff=True, is_superuser=True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null=True)

    is_seller = models.BooleanField(default=False)
    national_code = models.CharField(max_length=10, blank=True, null=True, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.get_full_name()} ({self.phone})'

    class Meta:
        db_table = 'custom_users'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['created_at']), models.Index(fields=['updated_at'])]


class Address(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    address = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.province}, {self.city} ({self.custom_user.get_full_name()})'

    class Meta:
        db_table = 'address'
        ordering = ['created_at']
        indexes = [models.Index(fields=['created_at']), models.Index(fields=['updated_at'])]