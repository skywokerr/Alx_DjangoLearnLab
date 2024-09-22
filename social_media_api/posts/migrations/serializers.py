from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment,Like
from rest_framework.serializers import ValidationError

#Step 2: Implement Serializers for Posts and Comments
# Serializer Setup:
# Create serializers for both Post and Comment in posts/serializers.py.
# Ensure that serializers handle user relationships correctly and validate data as needed.


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    post = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id',"content",'author','post']

class PostSerializer(serializers.ModelSerializer):
    #We want to make sure we can also pass the comments within each post
    comments = CommentSerializer(many=True,required=False)
    # author = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','title','content','comments','author']
    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "username": obj.author.username,  #This method aims to get key details for the user so that I can pass them as output for userfeed
            "email": obj.author.email
        }
    def validate_title(self, value):
        if len(value)<5:
            raise ValidationError("Title needs to be longer than five characters")
        return value
    # def validate(self, data):
    #     #here, I am trying to get the request information so that I can access the current user
    #     request = self.context.get('request')
    #     if request and request.user != data['author']:
    #         raise ValidationError("You cannot create another user's post")
    #     return data
    #since we are adding comments from a separate model, we need to override the create method
    def create(self, validated_data):
        #first, we want to get comment data. We also add an empty list in case there are no comments at the time
        comments_data = validated_data.pop('comments',[])
        #The next step is to create the new post
        post = Post.objects.create(**validated_data) #it expects kwargs, which is why we do **validated data
        #we then want to create comments within each post using a for loop
        for comment_data in comments_data:
            Comment.objects.create(post=post,**comment_data)
        #we then return the post with the comments within it
        return post
    #we also need to make sure it is possible to update comments within the post
    #we override the update method
    def update(self, instance, validated_data):
        #first we get comment data
        comments_data = validated_data.get('comments', None)
        #we then get the instances we want to edit from the blog post
        instance.title = validated_data.get('title',instance.title)
        instance.content = validated_data.get('content',instance.content)
        instance.save()
        #we also want to make it possible to change the comment details as well
        #here, I check to ensure that if data is none, it cannot be iterated through
        if comments_data is not None:
            
            for comment_data in comments_data:
                comment_id = comment_data.get('id')
                #if the comment is present, we retrieve it
                if comment_id:
                    comment = Comment.objects.get(id=comment_id,post=instance)
                    #for comment, we only want to change the content
                    comment.content = comment_data.get('content',comment.content) #we add comment.content in case we don't want to make any changes
                    comment.save()
                # else:
                    
                    # #we want to create a new comment
                    # Comment.objects.create(post=instance,**comment_data)
        return instance

class LikeSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at','number_of_likes']
        
    def get_number_of_likes(self,obj):
        return obj.post.post_likes.count()
        