from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
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
    objects = UserManager()
class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name='books')
    def __str__(self):
        return self.title
    class Meta:
        permissions = [("can_add_book", "Can_add_book"),("can_change_book", "Can_change_book"),("can_delete_book", "Can_delete_book")]

class Library(models.Model):
    name = models.CharField(max_length=100, null=False)
    books = models.ManyToManyField(Book, related_name='library')
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100, null=False)
    library = models.OneToOneField(Library,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
]
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15,choices=ROLE_CHOICES, default='Member')
    def __str__(self):
        return f'{self.user.username} - {self.role}'
