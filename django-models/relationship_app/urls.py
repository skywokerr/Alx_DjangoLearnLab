from django.urls import path
from .views import list_books, LibraryDetailView,login,index,SignUpView, admin_view,member_view,librarian_view,edit_book,delete_book,add_book
from . import views
from django.contrib.auth.views import LogoutView, LoginView
app_name = 'relationship_app'
urlpatterns = [
   path('books/', list_books, name='books'), 
    path('<int:id>/', LibraryDetailView.as_view(), name='library'),
    path('home/',index, name='index'),
    path('registration/',views.register,name='registration'),
    path('login/',login, name='login'),
    path('logout/',LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout' ),
    path('logout/',LoginView.as_view(template_name='relationship_app/login.html'), name='login' ),
     path('admin/', admin_view,name='adminview'),
    path('librarian/',librarian_view,name='librarianview'),
    path('member/',member_view,name='memberview'),
    path('add_book/',add_book, name='add_book'),
    path('edit_book/<int:id_book>/', edit_book, name='edit_book'),
    path('delete_book/<int:id_book>/', delete_book, name='delete_book'),
   
]
