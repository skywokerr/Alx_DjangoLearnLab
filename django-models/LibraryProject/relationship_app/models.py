from django.db import models
from django.contrib.auth.models import User
# Create your models here.
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
