from rest_framework import serializers
from django.utils import timezone
from .models import Book, Author, BookInstance, Genre


class AuthorsSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    second_name = serializers.CharField()


class AuthorSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    second_name = serializers.CharField()
    gender = serializers.CharField()
    date_of_birth = serializers.DateField()
    date_of_death = serializers.DateField()


class AuthorBoooksSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class BooksSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = serializers.CharField()
    title = serializers.CharField()
    isbn = serializers.CharField()
    summary = serializers.CharField()
    language = serializers.CharField()


class BooksInstanceSerializer(serializers.Serializer):
    id = serializers.CharField()
    book = serializers.CharField()
    publishing_year = serializers.CharField()
    status = serializers.CharField()
    due_back = serializers.DateField()
    borrower = serializers.CharField()
