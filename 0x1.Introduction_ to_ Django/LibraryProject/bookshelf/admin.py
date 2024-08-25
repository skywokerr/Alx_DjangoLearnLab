from django.contrib import admin

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'publication_year')
    list_filter = ('title','author','publication_year')
    search_fields = ('title','author')