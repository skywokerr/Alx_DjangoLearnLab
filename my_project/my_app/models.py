from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_lenghth = 200)
    author = models.CharField(max_lenghth = 100)
    published_date = models.DateField()
    