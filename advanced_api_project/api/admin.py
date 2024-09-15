from django.contrib import admin
from .models import Book, Author

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['author','title','publication_year']
