from .models import Book
from rest_framework import serializers
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title','author']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','email']