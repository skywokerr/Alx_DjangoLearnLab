from django.shortcuts import render
from rest_framework import generics
from .models import Mymodel
from serilaizers import MymodelSerializer


# Create your views here.
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer