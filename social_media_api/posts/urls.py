from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet,CommentViewSet,user_feed,Unlike_Post,Like_Post

router = DefaultRouter()
router.register(r'posts',PostViewSet,basename='posts')
router.register(r'comments',CommentViewSet,basename='comments')
urlpatterns = [
    path('',include(router.urls)),
    path('userfeed/',user_feed,name='userfeed'),
    path('posts/<int:pk>/like/',Like_Post.as_view(),name='like_post'),
    path('posts/<int:pk>/unlike/',Unlike_Post.as_view(),name='unlike_post'),
]