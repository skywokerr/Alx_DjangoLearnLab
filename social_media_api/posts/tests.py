from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from .views import PostViewSet,CommentViewSet
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Post,Like
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
# Create your tests here.

#We now need to test these viewsets
#first, we create a class and set it up

class TestViews(APITestCase):
    def setUp(self):
        #first call the client object from apiclient class
        self.client = APIClient()
        #I then create a reverse for the urls
        #when using viewsets, we have an option to add -detail or -list. -detail is to see a single post, while list include post, put, and get
        self.posts_url = reverse('posts-list')
        self.login_user_url = reverse('login_user')
        self.comments_url = reverse('comments-list')
        #we first create the first user
        self.user1 = get_user_model().objects.create_user(
            username= 'Martin',
            email='martin@gmail.com',
            password='Martin1234.',
            date_of_birth = '2011-11-11',
            first_name = 'Martin',
            last_name = 'Junior'
            
        )
        #we then create the second user
        self.user2 = get_user_model().objects.create_user(
            username= 'Lawrence',
            email='lawrence@gmail.com',
            password='Lawrence1234.',
            date_of_birth = '2011-11-11',
            first_name = 'Lawrence',
            last_name = 'Junior'
            
        )
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        self.client.post(self.posts_url,{
            "title":"This is the first test post for liking and unliking",
            "content":"This is the content for this test post for liking and unliking"
        })
        self.client.post(self.posts_url,{
            "title":"This is the second test post for liking and unliking",
            "content":"This is the second post content for liking and unliking"
        })
        self.client.logout()
    #the first step is to test post creation.
    def test_post_creation(self):
        self.client.login(email='lawrence@gmail.com',password='Lawrence1234.')
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        response_data = response.json()
        print(response_data['title'])
        #I am checking in the jsonified data when title matches with what I have shared.
        self.assertEquals(response_data['title'],'This is the first test post')
    #next, I want to test whether a comment is created successfully.
    def test_comment_creation(self):
        self.client.login(email='lawrence@gmail.com',password='Lawrence1234.')
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
      #I have obtained the post
        post = Post.objects.get(title="This is the first test post")
        post_id = post.id #I have then obtained the id of the post
        print(post_id)
        response = self.client.post(self.comments_url,{
            "post_id": post_id, #I used post_id because It is referenced in the view as post_id where I get it from request data
            "content":"This is the content for this first comment"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #examine notification after comment has been created
        
    def test_validate_length_of_title(self):
        self.client.login(email='lawrence@gmail.com',password='Lawrence1234.')
        response = self.client.post(self.posts_url,{
            "title":"This", #I am testing if when I type an title less than 5 characters I get an error.
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    #I have to now test put and then delete
    def test_update_post(self):
        #first, we login since the user is the author of the post
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #first, we have to create a post
        response = self.client.post(self.posts_url,{
            "title":"This is the original post", #I am testing if when I type an title less than 5 characters I get an error.
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #get the id of the post
        post_id = response.data['id']
        #create a reverse url
        self.update_post_url = reverse('posts-detail',args=[post_id])
        #we then update this particular post
        response = self.client.put(self.update_post_url,{
            "title":"this is the updated version of the original post",
            "content":"This is the content for this updated post"
        })
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        print(response.data['title'])
        #we then assert to see if details and status code matches
    def test_update_comment(self):
        #first we login
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #we then create a post to be associated with the comment
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then obtain the id of the post
        post = Post.objects.get(title="This is the first test post")
        post_id = post.id #I have then obtained the id of the post
        print(post_id)
        #we first create the comment
        response = self.client.post(self.comments_url,{
            "post_id": post_id, #I used post_id because It is referenced in the view as post_id where I get it from request data
            "content":"This is the content for this first comment"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then update the comment
        #we get the comment id
        comment_id = response.data['id']
        print(f"comment_id is {comment_id}")
        #create a reverse url for comment
        self.update_comment_url = reverse('comments-detail',args=[comment_id])
        #we then update this particular post
        response = self.client.put(self.update_comment_url,{
            "content":"This is the updated comment"
        })
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        print(response.data['content'])
        #we then assert to see if details and status code matches
    def test_delete_post(self):
        #first we log in
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #we then create the post to be deleted
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we get the id of the post
        post_id = response.data['id']
        #create a reverse url
        self.delete_post_url = reverse('posts-detail',args=[post_id])
        #we then perform delete
        response = self.client.delete(self.delete_post_url)
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
    def test_delete_comment(self):
        #first we login
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #we then create a post to be associated with the comment
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then obtain the id of the post
        post = Post.objects.get(title="This is the first test post")
        post_id = post.id #I have then obtained the id of the post
        print(post_id)
        #we first create the comment
        response = self.client.post(self.comments_url,{
            "post_id": post_id, #I used post_id because It is referenced in the view as post_id where I get it from request data
            "content":"This is the content for this first comment"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then update the comment
        #we get the comment id
        comment_id = response.data['id']
        print(f"comment_id is {comment_id}")
        #create a reverse url for comment
        self.delete_comment_url = reverse('comments-detail',args=[comment_id])
        #we then update this particular post
        response = self.client.delete(self.delete_comment_url,)
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
    def test_user_feed(self):
        #we first login to get authenticated
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #we then create two posts with this user as the author
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we create post 2
        response = self.client.post(self.posts_url,{
            "title":"This is the second post",
            "content":"This is the content for second post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then logout this user
        self.client.logout()
        #we then login the next user
        response = self.client.post(self.login_user_url,{
            "email":"lawrence@gmail.com",
            "password":"Lawrence1234.",
        })
        #we then implement follow logic
        token = response.data.get('token')
        print(f"Token for Lawrence: {token}")
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        #we now need to follow another user
        User = get_user_model()
        user_to_follow = User.objects.get(username='Martin')
        user_id = user_to_follow.id
        print(f"Martin to be followed user id: {user_id}")
        #we now need to follow this user
        self.follow_url = reverse('following',args=[user_id])
        response = self.client.post(self.follow_url)
        print(response.data)
        self.assertEquals(response.status_code,status.HTTP_202_ACCEPTED)
        user_following = User.objects.get(username='Lawrence')
        following_count = user_following.following.all().count() #It tracks number of followers the user has
        print(f"number of people Lawrence is following: {following_count}")
        #We now need to test userfeed
        user_feed_url = reverse('userfeed')  # URL for the feed in the posts app
        response = self.client.get(user_feed_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        #we may also want to see the content
        for post in response.data:
            self.assertEquals(post['author']['username'],'Martin') #here, I want to see whether the author for each post is martin
            print(post) #here, I want to see whether posts are printed
    def test_like_post(self):
        #first we login
        response = self.client.post(self.login_user_url,{
            "email":"lawrence@gmail.com",
            "password":"Lawrence1234.",
        })
        
        #we get the token
        token = response.data.get('token')
        print(f"Token for Lawrence during like post: {token}")
        #we authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        #we start the test
        #first we get the post
        post = Post.objects.get(title="This is the first test post for liking and unliking")
        pk = post.id
        print(f"This is the first post id for liking post: {pk}")
        self.like_notify_url = reverse('like_post',args=[pk])
        response=self.client.post(self.like_notify_url)
        print(f"response data for liking post: {response.data}")
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we get whether the post like number has changed
        number_of_likes = post.post_likes.all().count()
        print(f"the number of likes for the first post: {number_of_likes}")
    def test_unlike_post(self):
        #first we login
        response = self.client.post(self.login_user_url,{
            "email":"lawrence@gmail.com",
            "password":"Lawrence1234.",
        })
        
        #we get the token
        token = response.data.get('token')
        print(f"Token for Lawrence during like post: {token}")
        #we authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        #we start the test
        #we must first like the post
        post = Post.objects.get(title="This is the first test post for liking and unliking")
        pk = post.id
        print(f"This is the first post id for liking post: {pk}")
        self.like_notify_url = reverse('like_post',args=[pk])
        response=self.client.post(self.like_notify_url)
        print(f"response data for liking post before unliking: {response.data}")
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we get whether the post like number has changed
        number_of_likes = post.post_likes.all().count()
        print(f"the number of likes for the first post before unliking: {number_of_likes}")
        
        #first we get the post
        post = Post.objects.get(title="This is the first test post for liking and unliking")
        pk = post.id
        print(f"This is the first post id for liking post: {pk}")
        self.unlike_notify_url = reverse('unlike_post',args=[pk])
        response=self.client.post(self.unlike_notify_url)
        print(f"response data for unliking post: {response.data}")
        self.assertEquals(response.status_code,status.HTTP_202_ACCEPTED)
        #we get whether the post like number has changed
        number_of_likes = post.post_likes.all().count()
        print(f"the number of likes for the first post: {number_of_likes}")
    def test_comment_recipient_notification(self):
        response = self.client.post(self.login_user_url,{
            "email":"lawrence@gmail.com",
            "password":"Lawrence1234.",
        })
        
        #we get the token
        token = response.data.get('token')
        print(f"Token for Lawrence during comment notify recipient: {token}")
        #we authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
      #I have obtained the post
        post = Post.objects.get(title="This is the first test post for liking and unliking")
        post_id = post.id #I have then obtained the id of the post
        print(post_id)
        response = self.client.post(self.comments_url,{
            "post_id": post_id, #I used post_id because It is referenced in the view as post_id where I get it from request data
            "content":"This is the content for this first comment for testing notification"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #examine notification after comment has been created
        #author of the retrieved post is Michael
        self.client.logout()
        
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        user = get_user_model().objects.get(email='martin@gmail.com')
        self.notification_url = reverse('user notifications')
        total_notifications = user.recipient_notifications.all().count()
        print(f'total notifications for michael: {total_notifications}')
        response = self.client.get(self.notification_url)
        print(f'response data for notifications for michael: {response.data}')
        
