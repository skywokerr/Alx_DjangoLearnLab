from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password,date_of_birth,profile_photo):
        if not email:
            raise ValueError("You must have an email")
        if not date_of_birth:
            raise ValueError("You must provide a birth date")
        if not profile_photo:
            raise ValueError("You must provide a profile pic")
        user = self.model(email=self.normalize_email(email),date_of_birth=date_of_birth,profile_photo=profile_photo)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password,date_of_birth,profile_photo):
        user = self.create_user(email,password,date_of_birth,profile_photo)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    email = models.EmailField(max_length=155, unique=True)
    username = models.CharField(max_length=100, unique=False)
    date_of_birth = models.DateField(blank=True, default=timezone.now)
    profile_photo = models.ImageField(blank=True)
    
    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','profile_photo']
    objects = CustomUserManager()
class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return f"Title: {self.title} Author: {self.author} Publication Year: {self.publication_year}"
    class Meta:
        permissions = [("can_view", "Can_view"),("can_create","Can_create"),("can_edit","Can_edit"),("can_delete","Can_delete")]