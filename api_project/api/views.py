from django.shortcuts import render,get_object_or_404
from .models import Book
from .serializers import BookSerializer,UserSerializer
import rest_framework
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.

class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
class ListCreateBookView(ListCreateAPIView):
    permission_classes=[IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
@api_view(['GET'])
def get_view(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"Details":"Not Found"},status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(instance=user)
    return Response({"user":serializer.data})
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({"user":serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer