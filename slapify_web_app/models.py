from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, user_type='User', **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_type=user_type, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, user_type='Admin', **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, email, password, **kwargs)

class User(AbstractUser):
    user_type_choices = (
        ('Admin', 'Admin'),
        ('Artist', 'Artist'),
        ('User', 'User'),
    )
    user_type = models.CharField(max_length=20, choices=user_type_choices, default='User')

    objects = UserManager()

    class Meta:
        permissions = [
            ('can_view_special_content', 'Can view special content'),
        ]
     # Define related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_slapifyuser_groups',
        related_query_name='custom_slapifyuser_group' 
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_slapifyuser_user_permissions', 
        related_query_name='custom_slapifyuser_user_permission'
    )