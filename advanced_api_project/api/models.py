from django.db import models

# Create your models here.
"""
Step 3: Define Data Models
Model Requirements:

Create two models, Author and Book.
The Author model should have the following fields:
name: a string field to store the author’s name.
The Book model should have the following fields:
title: a string field for the book’s title.
publication_year: an integer field for the year the book was published.
author: a foreign key linking to the Author model, establishing a one-to-many relationship from Author to Books.
"""
#Model Author. 
#This model allows the creation of an author instance. It has the attribute name.
# It also has the str method to return the name of the author when the instance is called
class Author(models.Model):
    name = models.CharField(max_length=100,null=False, verbose_name="Author's Name")
    def __str__(self):
        return self.name
#Model Book. 
#This model allows the creation of a book instance. It has the attribute author, a foreign key inheriting the Author model.
#it also has the title and publication year. I have added the related_name so that the serializers can retrieve the books belonging to a specific author
# It also has the str method to return the name of the author when the instance is called
class Book(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')
    title = models.CharField(max_length=100,null=False,verbose_name='Book Title')
    publication_year = models.IntegerField(null=False)