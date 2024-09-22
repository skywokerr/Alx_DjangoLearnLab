from django.shortcuts import render,get_object_or_404
from .serializers import PostSerializer,CommentSerializer,LikeSerializer
from .models import Post,Comment,Like
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import filters
from rest_framework.decorators import permission_classes,api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from notifications.models import Notification
from rest_framework.generics import get_object_or_404
# generics.get_object_or_404(Post, pk=pk) Checker
# Like.objects.get_or_create(user=request.user, post=post) Checker
User = get_user_model()
# Create your views here.
#Step 3: Create Views for CRUD Operations
# View Implementation:
# Using Django REST Framework’s viewsets, set up CRUD operations for both posts and comments in posts/views.py.
# Implement permissions to ensure users can only edit or delete their own posts and comments.
#I want to create a custom permission that will allow me to determine who can make changes and who cannot
class ReadOnlyPostComments(BasePermission):
    #I am using object permission because I want access to post and comment objects
    def has_object_permission(self, request, view, obj):
        #here I am checking whether the method include get,options, and head
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user #here, I am assigning the rights for other methods to the user if they are the author
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,ReadOnlyPostComments]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    def perform_create(self, serializer):
        #here, I want to influence what the serializer can do. I want it to save the author directly
        serializer.save(author=self.request.user)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,ReadOnlyPostComments]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']
    def perform_create(self, serializer):
        #here, I want to influence what the serializer can do. I want it to save the author directly
        #here, I have added additional context to ensure I am getting the exact post. I am saying from request.data. get the post_id
        #Then, I am retrieving the post and saving it as part of the serializer
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user,post=post)
         # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,
            actor=self.request.user,
            verb=2,  # 'Comment' as per notification types
            target=post,
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id,
            text_preview=post.content
        )
   
""""
Step 5: Implement Pagination and Filtering
Enhance API Usability:
Add pagination to post and comment list endpoints to manage large datasets.
Implement filtering capabilities in post views to allow users to search posts by title or content.
"""
"""
Step 3: Implement the Feed Functionality
Feed Generation:
Create a view in the posts app that generates a feed based on the posts from users that the current user follows.
This view should return posts ordered by creation date, showing the most recent posts at the top.
"""
#first we authenticate
@permission_classes([permissions.IsAuthenticated])
#we get api decorate users_followed_by_current_user
@api_view(['GET'])
def user_feed(request):
    following_users = request.user.following.all() #here we are getting all users the user follows
    #we need now to get the posts
    posts_by_these_following_users = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts_by_these_following_users,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

#we create a view to handle liking of a post and also notifications of the same
class Like_Post(generics.GenericAPIView):
    #first, the user must be authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,pk):
        #first we get the post
        post = get_object_or_404(Post,id=pk)
        like, created = Like.objects.get_or_create(post=post,user=request.user)
        #we call notifications after user has been created
        if created:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb=1, #I used this because it is what is in my notification types
                target=post,
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id,
                text_preview=post.content
                
            )
            like_serializer = LikeSerializer(like)
            return Response({"like":like_serializer.data,"message":f"post liked by {request.user.username}"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"You have already liked this post"})
        
class Unlike_Post(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self,request,pk):
        #we first get the post that was liked
        post = get_object_or_404(Post,id=pk)
        #we get the like
        like = Like.objects.get(post=post,user=request.user)
        if like:
            like.delete()
            return Response({"You have unliked":f"{post.title}"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"You have not yet liked":f"{post.title}"},status=status.HTTP_404_NOT_FOUND)