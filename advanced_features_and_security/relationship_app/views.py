from typing import Any
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library,Book
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.views.generic import DetailView,TemplateView,ListView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from .forms import BookForm
# Create your views here.
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/books/')
        else:
            form = BookForm()
        return render(request, 'relationship_app/add_book.html', {'form':form})
@permission_required('relationship_app.can_change_book')
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
@permission_required('relationship_app.can_delete_book')
def delete_book(request, id_book):
    book = Book.objects.get(pk=id_book)
    if request.method == 'POST':
        book.delete()
        return redirect('/books/')
    return render(request, 'relationship_app/edit_book.html', {'book': book})
def list_books (request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request,'relationship_app/list_books.html',context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# Create your views here.
class register(CreateView):
    form_class = UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'
    
def login (request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/books/')  #redirects user towards the books page.
            else:
                return HttpResponse("Invalid credentials", status=401)
        else:
            return HttpResponse("Invalid form data", status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})
    
def index(request):
    return render(request, 'relationship_app/index.html')

# def Admin(user):
#     return hasattr(user,'userprofile') and user.userprofile.role == 'Admin'
# def Librarian(user):
#     return hasattr(user,'userprofile') and user.userprofile.role == 'Librarian'
# def Member(user):
#     return hasattr(user,'userprofile') and user.userprofile.role == 'Member'

# @user_passes_test(Admin)
# def admin_view(request):
#     if not request.user.userprofile.role == 'Admin':
#         return HttpResponseForbidden("You have no access to this page.")
#     context = {'message': 'Welcome to the admin view!'}
#     return render(request, 'relationship_app/admin_view.html',context)
# @user_passes_test(Librarian)
# def librarian_view(request):
#     if not request.user.userprofile.role == 'Librarian':
#         return HttpResponseForbidden("You have no access to this page.")
#     context = {'message': 'Welcome to the librarian view!'}
#     return render(request, 'relationship_app/librarian_view.html', context)
# @user_passes_test(Member)
# def member_view(request):
#     if not request.user.userprofile.role == 'Member':
#         return HttpResponseForbidden("You have no access to this page.")
#     context = {'message': 'Welcome to the librarian view!'}
#     return render(request, 'relationship_app/member_view.html')
def check_role(user, role):
  return user.is_authenticated and user.userprofile.role == role

@user_passes_test(lambda user: check_role(user, "Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(lambda user: check_role(user, "Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(lambda user: check_role(user, "Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")