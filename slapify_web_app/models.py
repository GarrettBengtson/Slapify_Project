from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
# import to support mp3 playing
from mutagen.mp3 import MP3

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

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    # types for genre
    genre_choices = (
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Classical', 'Classical'),
        ('Rap', 'Rap'),
        ('Alt', 'Alt'),
        ('Indie', 'Indie'),
        ('Other', 'Other')
    )
    genre = models.CharField(max_length=20, choices=genre_choices, default='Other')
    song_file = models.FileField(upload_to='songs/')
    duration_minutes = models.IntegerField(blank=True, null=True)
    duration_seconds = models.IntegerField(blank=True, null=True)

    # calculate the audio and duration using the uploaded song_file
    # save these to the Song object
    def save(self, *args, **kwargs):
        if self.song_file.name.endswith('.mp3'):
            audio = MP3(self.song_file)
            duration_in_seconds = audio.info.length
            # parsing to determine the proper time to display
            self.duration_minutes = int(duration_in_seconds // 60)
            self.duration_seconds = int(duration_in_seconds % 60)
        # incorrect file type
        else:
            self.duration_minutes = None
            self.duration_seconds = None 

        super().save(*args, **kwargs)

    def formatted_duration(self):
        if self.duration_minutes is not None and self.duration_seconds is not None:
            return f"{self.duration_minutes:02d}:{self.duration_seconds:02d}"
        else:
            return "N/A"


    def __str__(self):
        return self.title

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name