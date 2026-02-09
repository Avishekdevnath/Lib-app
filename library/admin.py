from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'biography']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'availability_status', 'available_copies', 'total_copies']
    list_filter = ['category', 'availability_status']
    search_fields = ['title', 'author__name']
