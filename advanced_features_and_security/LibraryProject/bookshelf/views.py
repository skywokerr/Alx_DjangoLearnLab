from typing import Any
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import DetailView,TemplateView,ListView, CreateView
from .models import Librarian,Library,Author,Book
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from .forms import BookForm,CustomUserCreationForm,CustomLoginForm
from django.contrib.auth.models import auth
from django.db.models import Q
from .forms import ExampleForm

# Create your views here.
@permission_required('book_list.can_view', raise_exception=True)
def book_List(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request,'relationship_app/book_list.html',context)
@permission_required('book_list.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/books/')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form':form})
@permission_required('book_list.can_edit', raise_exception=True)
def edit_book(request, id_book):
    book = Book.objects.get(pk=id_book)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid:
            form.save()
            return redirect('/books/')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})
@permission_required('book_list.can_delete', raise_exception=True)
def delete_book(request, id_book):
    book = Book.objects.get(pk=id_book)
    if request.method == 'POST':
        book.delete()
        return redirect('/books/')
    return render(request, 'relationship_app/edit_book.html', {'book': book})
def search_books(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
