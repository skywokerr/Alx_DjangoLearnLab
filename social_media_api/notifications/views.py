from django.shortcuts import render,get_object_or_404
from .models import Notification
from .serializer import NotifyRecipientSerializer
from rest_framework import permissions, generics, response,status
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

#we want to display notifications for the user and allow filtering by unread status
User = get_user_model()

class NotificationCollection(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend] #I learned that this is better when it comes to booleans
    filterset_fields = ['is_seen'] #allows users to search and filter based on whether is_seen is true or false
    def get(self, request):
        current_user = self.request.user
        
        # Log the filtering parameter
        is_seen_param = request.query_params.get('is_seen')
        print(f"Filtering notifications with is_seen={is_seen_param}")
        
        # Retrieve notifications, applying the filter if provided
        notifications = Notification.objects.filter(recipient=current_user)

        if is_seen_param is not None:
            # Convert to boolean for filtering
            is_seen_filter = is_seen_param.lower() == 'true'
            notifications = notifications.filter(is_seen=is_seen_filter) #here we are filtering results that are true

        notifications = notifications.order_by('-timestamp')

        # Serialize the notifications
        notification_serializer = NotifyRecipientSerializer(notifications, many=True)
        return response.Response({"user notifications": notification_serializer.data}, status=status.HTTP_200_OK)
    # def get(self,request):
    #     current_user = self.request.user
    #     if current_user:
    #         notifications = Notification.objects.filter(recipient=current_user).order_by('-timestamp')
            
    #         notification_serializer = NotifyRecipientSerializer(notifications,many=True) #many is true so that we return more than 1 notification
    #         return response.Response({"user notifications":notification_serializer.data},status=status.HTTP_200_OK)
    #     else:
    #         return response.Response({"Error ":"You are not authorized To access this page"},status=status.HTTP_401_UNAUTHORIZED)
#now I want to implement marking notifications as read
class MarkNotificationsAsRead(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,pk):
        notification = get_object_or_404(Notification,id=pk)
        if notification:
            notification.is_seen = True
            notification.save()
            return response.Response({"Success": f"Notification from {notification.actor.username} has been read"},status=status.HTTP_200_OK)
        else:
            return response.Response({"error":"Notification not found"},status=status.HTTP_404_NOT_FOUND)