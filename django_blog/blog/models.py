from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self,email,username,password,first_name,last_name):
#         if not email:
#             raise ValueError("Please provide an email")
#         if not username:
#             raise ValueError("Please provide a username")
#         user = self.model(
#             email=self.normalize_email(email),
#             username = username,
#             first_name = first_name,
#             last_name = last_name
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#     def create_superuser(self,email,username,password,first_name,last_name):
#         user = self.create_user(
#             email= self.normalize_email(email),
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             password=password
#         )
#         user.is_staff = True
#         user.is_admin = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
# class User(AbstractUser):
#     email = models.EmailField(unique=True,max_length=155)
#     username = models.CharField(unique=True,max_length=50)
#     first_name = models.CharField(unique=False,max_length=50)
#     last_name = models.CharField(unique=False,max_length=50)
    
#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
class Tag(models.Model):
    name = models.CharField(max_length=100)
class Post(models.Model):
    title = models.CharField(max_length=200, null=False, unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, max_length=100)
    tags= TaggableManager()
    
    def __str__(self):
        return f"Post Title {self.title} by {self.author.first_name} {self.author.last_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userprofile')
    bio = models.TextField()
    image_url = models.URLField(blank=True,null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.author.first_name} {self.author.last_name}"