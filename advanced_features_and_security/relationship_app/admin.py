from django.contrib import admin
from .models import Book, Author,Librarian,Library
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', )
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', )
