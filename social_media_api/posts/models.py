from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
#create a post model
class Post(models.Model):
#Post should have fields like author (ForeignKey to User), title, content, created_at, and updated_at.
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(verbose_name='Post Title',max_length=150,null=False,unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Author: {self.author.username} Title: {self.title}"
class Comment(models.Model):
    #Comment should reference both Post (ForeignKey) and User (author), with additional fields for content, created_at, and updated_at.
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='comments_by_author')
    content = models.CharField(max_length=300,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Post Referenced: '{self.post.title}' Author Referenced: '{self.author}'"
#we need to create a like model to manage likes
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_likes')
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='user_likes') #the one liking
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def postlikes(self):
        number_of_likes = self.post_likes.all().count()
        return str(number_of_likes)
    def userlikes(self):
        number_of_user_likes = self.user_likes.all().count()
        return str(number_of_user_likes)