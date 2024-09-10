from django.urls import path,include
from django.conf.urls import include
from .views import BookList, ListCreateBookView,get_view
from .views import BookViewSet,login,signup
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'bookviewset',BookViewSet,basename='bookviewset')

urlpatterns = [
    path('',include(router.urls)),
    path('api/books/create/',ListCreateBookView.as_view()),
    path('api/books/',BookList.as_view()),
    path('api/get_view/',get_view),
    path('login/',login),
    path('signup/',signup),
    path('api-token-auth/', obtain_auth_token)
]