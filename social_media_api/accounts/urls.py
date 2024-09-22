from django.urls import path,include
from .views import login,signup,UserProfileView,signup_user,login_user,follow_user,unfollow_user,ViewAllUsers
urlpatterns = [
    path('register/',signup,name='signup'),
    path('login/',login,name='login'),
    path('userprofile/',UserProfileView.as_view(),name='userprofile'),
    path('api_auth/',include('rest_framework.urls'),name='auth'),
    path('register_new_user/',signup_user,name='register'),
    path('login_user/',login_user,name='login_user'),
    path('follow/<int:user_id>/',follow_user,name='following'),
    path('unfollow/<int:user_id>/',unfollow_user,name='unfollow'),
    path('viewusers',ViewAllUsers.as_view(),name='viewusers'),
]