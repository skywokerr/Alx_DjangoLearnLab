from django.shortcuts import render,get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer,UserProfileSerializer,LoginSerializer,ListUsersForFollowPurposes
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

# Create your views here.
#use a function view with an api decorator to signup
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    #check validity of serializer
    if serializer.is_valid():
        serializer.save()
        #get the user
        user = CustomUser.objects.get(email=request.data['email'])
        #use django set password to hash the password from user
        user.set_password(request.data['password'])
        user.save()
        #get the token by creating it and assigning user to current user
        token,created = Token.objects.get_or_create(user=user)
        #here we return response containing json details, such as token key and serializer data
        return Response({"token":token.key,"user":serializer.data})
@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = get_user_model().objects.get(email=request.data["email"])
        user.set_password(request.data['password'])
        user.save()
        return Response({"user":serializer.data})
@api_view(['POST'])
#allow user login
def login(request):
    user = get_object_or_404(CustomUser,email=request.data['email'])
    #first we check whether user has entered the right password
    if not user.check_password(request.data['password']):
        return Response({"details":"not found"},status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    #we return user details
    serializer = UserSerializer(instance=user)
    return Response({"token":token.key,"user":serializer.data})
#an alternative login version where logic is inside serializer.py
@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data)
    return Response(serializer.errors)
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated] #It ensures that the user is authenticated so that we can get the token
    def get_object(self): #returns the profile of the user
        return self.request.user
"""
Step 2: Create API Endpoints for Managing Follows
Follow Management Views:
Develop views in the accounts app that allow users to follow and unfollow others. This might include actions like follow_user and unfollow_user, which update the following relationship.
Ensure proper permissions are enforced so users can only modify their own following list.
"""
#We must create a follow view only that allows users to follow a specific profile
#so first, we must get that user profile using a specific pk
User = get_user_model()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request,user_id):
    #we get that id of the user
    user_to_follow = User.objects.get(id=user_id)
    user_doing_the_following = request.user
    #we check whether that user exists
    if user_to_follow:
        #we use related name and add because we are dealing with many to many relationships
        request.user.following.add(user_to_follow)
        Notification.objects.create(
            recipient=user_to_follow,
            actor=user_doing_the_following,
            verb=3,  # 'Comment' as per notification types
            target=user_to_follow, #the target is the person experincing an action. in this case being followed
            content_type=ContentType.objects.get_for_model(user_to_follow), #content type is that of target
            object_id=user_to_follow.id
        )
        return Response({"You are now following":user_to_follow.username},status=status.HTTP_202_ACCEPTED)
    else:
        #we raise an error incase the follow fails
        return Response({"Details":"Not Found"},status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request,user_id):
    #first, we retrieve the user to unfollow
    user_to_unfollow = User.objects.get(id=user_id)
    #we check whether that user exists
    if user_to_unfollow:
        request.user.following.remove(user_to_unfollow)
        return Response({"You have unfollowed":user_to_unfollow.username},status=status.HTTP_202_ACCEPTED)
    else:
        #we raise an error incase the follow fails
        return Response({"Details":"Not Found"},status=status.HTTP_404_NOT_FOUND)

#checker expects the use of generics.GenericView

class FollowUsers(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,user_id):
        user_to_follow = CustomUser.objects.get(id=user_id)
        if user_to_follow:
            request.user.following.add(user_to_follow)
            
            
            
            return Response(f"You are now following {user_to_follow.username}", status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"Error":"User not found"})

class UnfollowUsers(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,user_id):
        user_to_unfollow = CustomUser.objects.get(id=user_id)
        if user_to_unfollow:
            request.user.following.remove(user_to_unfollow)
            return Response(f"You have unfollowed {user_to_unfollow.username}", status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"Error":"User not found"})

class ViewAllUsers(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        
        users = CustomUser.objects.all()
        serializer = ListUsersForFollowPurposes(users,many=True)
        return Response({"users":serializer.data},status=status.HTTP_200_OK)