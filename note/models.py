from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import List
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(
        default="images/avatar.svg", upload_to="images", null=True
    )
    REQUIRED_FIELDS: List[str] = []
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class SubjectList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubjectNote(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(SubjectList, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    file_upload = models.FileField(upload_to="files", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name
