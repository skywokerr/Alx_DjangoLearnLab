from django.urls import path
from .views import CreateView,ListView,DeleteView,UpdateView,DetailView
urlpatterns = [
    path("books/create",CreateView.as_view(),name='createview'),
    path("books",ListView.as_view()),
    path("books/delete/<int:pk>/",DeleteView.as_view(),name='deleteview'),
    path("books/update/<int:pk>/",UpdateView.as_view(),name='updateview'),
    path('detailview/<int:pk>/',DetailView.as_view()),
]