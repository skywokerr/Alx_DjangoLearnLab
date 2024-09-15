from django.urls import path
from .views import profileview,search,register,LoginUser,PostByTagListView,LogoutUser,home,CreatePostView,ListPostView,tagged,UpdatePostView,DeletePostView,DetailPostView,CommentCreateView,ListComment,CommentDeleteView,CommentDetail,CommentUpdateView


urlpatterns = [
    path('',home,name='home'),
    path('search/',search,name='search_results'),
    path('tags/<slug:tag_slug>/',PostByTagListView.as_view(),name='tagged_by_post'),
    path('register/',register,name='register'),
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(next_page='/'),name='logout'),
    path('profile/',profileview,name='profile'),
    path('post/new/',CreatePostView.as_view(), name='post_form'),
    path('posts/',ListPostView.as_view(),name='post_list'),
    path('post/<int:pk>/update/',UpdatePostView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/',DeletePostView.as_view(),name='post_confirm_delete'),
    path('post/<int:pk>/',DetailPostView.as_view(),name='post_detail'),
    path('post/<int:pk>/comments/new/',CommentCreateView.as_view(),name='comment_form'),
    path('posts/<int:post_id>/comments/list',ListComment.as_view(), name='comment_list'),
    # path('posts/<int:post_id>/comment/<int:comment_pk>/update',UpdateComment.as_view(),name='edit_comment'),
    path('comment/<int:pk>/update/',CommentUpdateView,name='edit_comment'),
    path('comment/<int:pk>/delete/',CommentDeleteView.as_view(), name='delete_comment'),
    path('comment/<int:pk>/',CommentDetail.as_view(),name='comment_detail'),
    path('tag/tag_name/<slug:slug>/',tagged,name='tagged')
]