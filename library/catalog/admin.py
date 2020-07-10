from django.contrib import admin

# Register models
from .models import Author, Genre, Book, BookInstance

admin.site.register(Genre)

class BooksInline(admin.TabularInline):
    model = Book
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'second_name', 'gender', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', 'second_name', 'gender', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Register the Admin classes for Book using the decorator
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """
    Administration object for BookInstance models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """
    list_display = ('book', 'publishing_year', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('publishing_year', 'status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','publishing_year', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
