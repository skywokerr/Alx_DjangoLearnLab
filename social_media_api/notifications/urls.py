from django.urls import path
from .views import NotificationCollection,MarkNotificationsAsRead

urlpatterns = [
    path('notifications/',NotificationCollection.as_view(),name='user notifications'),
    path('notifications/<int:pk>/',MarkNotificationsAsRead.as_view(),name='read notifications'),
]