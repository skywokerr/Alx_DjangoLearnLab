from django.test import TestCase
from .views import signup,login,UserProfileView,signup_user,login_user,follow_user,unfollow_user
from rest_framework.test import APIRequestFactory,APIClient,APITestCase
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework import status
from notifications.models import Notification
# Create your tests here.
#setUp allows us to initialize important details
class TestViews(APITestCase):
    def setUp(self):
        #we first get the client object from APIClient()
        #we then use reverse to reverse urls based on the assigned named
        self.client = APIClient()
        self.register_url = reverse('signup')
        self.login_url = reverse('login')
        self.profile_url = reverse('userprofile')
        self.auth_url = 'api_auth/'
        self.signup_user_url = reverse('register')
        self.login_user_url = reverse('login_user')
        
        #here, I am creating a new user using the Customuser model
        self.new_user = CustomUser.objects.create_user(
            username="Michael",
            email="michael@gmail.com",
            date_of_birth = "2011-11-11",
            first_name="Michael",
            last_name= "James",
            password="Michael1234.",
            
        )
        self.new_user1 = CustomUser.objects.create_user(
            username="annex",
            email="annex@gmail.com",
            date_of_birth = "2011-11-11",
            first_name="Ann",
            last_name= "Janie",
            password="Michael1234.",
            
        )
        User = get_user_model()
        self.newuser2 = User.objects.create_user(username="Lawrence",
            email="lawssen@gmail.com",
            date_of_birth = "2011-11-11",
            first_name="Manys",
            last_name= "Johns",
            password="Michael1234.",)
    #I first tested the register of the new user
    def test_register_new_user(self):
        #I use the post method and pass the register url and the json details
        response = self.client.post(self.register_url,{
            "username":"Alex",
            "email":"alex@gmail.com",
            "password":"ALEX1234.",
            "first_name":"Alex",
            "last_name":"Guandaru",
            "date_of_birth":"2011-11-11",
            "bio":"",
            "profile_picture":""
            })
        #I then assertequals the response code I should expect
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        user = CustomUser.objects.get(email="alex@gmail.com")
        
        print(user.id)
        #here, I am trying to get specific details from the user, such as username and first name
        self.assertIn('username',response.data['user'])
        self.assertEquals(response.data['user']['username'],'Alex')
        self.assertIn('first_name',response.data['user'])
        self.assertEquals(response.data['user']['first_name'],'Alex')
        #here, I am testing logging in by using the post method and passing the login url and the asserting equals and in
    def test_login_new_user(self):
        response = self.client.post(self.login_url,{
            "email":"michael@gmail.com",
            "password":"Michael1234."
        })
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertIn("username",response.data["user"]) #we check whether username is in the response data under user section
        self.assertIn("last_name",response.data["user"]) #we check whether last_name is in the response data under user section
        self.assertEquals(response.data["user"]["username"],"Michael") #we check whether user can receive their data after login
        self.assertEquals(response.data["user"]["last_name"],"James") #we check whether user can receive their data after login
    #I then tested another new user
    def test_new_login_user(self) :
        self.user = self.client.post(self.register_url,{
            "username":"janes",
            "email":"janes@gmail.com",
            "password":"Anne1234.",
            "first_name":"Anna",
            "last_name":"baracks",
            "date_of_birth":"2011-11-11",
            "bio":"",
            "profile_picture":"",
            })
        response = self.client.post(self.login_url,{"email":"janes@gmail.com", "password":"Anne1234."})
        self.assertEquals(response.status_code,status.HTTP_200_OK) 
        token = response.data.get('token') #retrieves the token from user data
      
        print(token)  
        self.assertIsNotNone(token) #checks to see whether user token is empty
    #This was a nightmare because of the token. but I figured it out
    def test_user_profile_user(self):
        #we first login the user and get the token
        response = self.client.post(self.login_url, {
            'email': 'michael@gmail.com',
            'password': 'Michael1234.'
        })
        token = response.data.get('token')
        
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #we use http_authorization
        response = self.client.get(reverse('userprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("email",response.data)
        # self.assertIn("username",response.data["user"])
        self.assertEquals(response.data["email"],"michael@gmail.com")
        # self.assertEquals(response.data['user']['username'],'Michael')
    #I tested another user here
    def test_another_user_profile(self):
        self.second_user = self.client.post(self.register_url,{
            "username":"Johnte",
            "email":"johnie@gmail.com",
            "password":"Johnie1234.",
            "first_name":"John",
            "last_name":"Lawrence",
            "date_of_birth":"2011-11-11",
            "bio":"This is a test",
            "profile_picture":"https://i.pinimg.com/originals/5a/72/9c/5a729ca9a4a4020c7090cc87665b7549.jpg"
            })
        response = self.client.post(self.login_url, {
            'email': 'johnie@gmail.com',
            'password': 'Johnie1234.'
        })
        token = response.data.get('token')
        print(f"Token for jonte: {token}")
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(reverse('userprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("email",response.data)
        # self.assertIn("username",response.data["user"])
        self.assertEquals(response.data["email"],"johnie@gmail.com")
    def test_new_user_sign_up(self):
        response = self.client.post(self.signup_user_url,{
            "username":"Manny",
            "email":"manny@gmail.com",
            "password":"Johnie1234.",
            "first_name":"Manny",
            "last_name":"Laws",
            "date_of_birth":"2011-11-11",
            "bio":"This is a test",
            "profile_picture":"https://i.pinimg.com/originals/5a/72/9c/5a729ca9a4a4020c7090cc87665b7549.jpg"
            })
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertIn('username',response.data["user"])
        self.assertEquals(response.data["user"]['username'],'Manny')
    #This login is the one in the serializer, where I use serializers.Serializer. 
    def test_new_login_method(self):
        #here we are first signing up the new user
        self.client.post(self.signup_user_url,{
            "username":"Manny",
            "email":"manny@gmail.com",
            "password":"Johnie1234.",
            "first_name":"Manny",
            "last_name":"Laws",
            "date_of_birth":"2011-11-11",
            "bio":"This is a test",
            "profile_picture":"https://i.pinimg.com/originals/5a/72/9c/5a729ca9a4a4020c7090cc87665b7549.jpg"
            })
        #we are then loggin in this user
        response = self.client.post(self.login_user_url,{
            "email":"manny@gmail.com",
            "password":"Johnie1234.",
        })
        #we then assert that the responses are correct
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertIn('email',response.data)
        self.assertEquals(response.data["email"],"manny@gmail.com")
    def test_follow_new_user(self):
        #first we log in the user
        response = self.client.post(self.login_user_url,{
            "email":"michael@gmail.com",
            "password":"Michael1234.",
        })
        # self.client.login(email="michael@gmail.com",password="Michael1234.")
        token = response.data.get('token')
        print(f"Token for Michael: {token}")
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        #we now need to follow another user
        User = get_user_model()
        user_to_follow = User.objects.get(username='Lawrence')
        user_id = user_to_follow.id
        print(f"Lawrence user id: {user_id}")
        #we now need to follow this user
        self.follow_url = reverse('following',args=[user_id])
        response = self.client.post(self.follow_url)
        print(response.data)
        self.assertEquals(response.status_code,status.HTTP_202_ACCEPTED)
        user_following = User.objects.get(username='Michael')
        following_count = user_following.following.all().count() #It tracks number of followers the user has
        print(f"number of people Michael is following: {following_count}")
    def test_unfollow_user(self):
        #first we login
        response = self.client.post(self.login_user_url,{
            "email":"michael@gmail.com",
            "password":"Michael1234.",
        })
        token = response.data.get('token')
        print(f"Token for Michael: {token}")
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        #we then follow a user
        #we now need to follow another user
        User = get_user_model()
        user_to_follow = User.objects.get(username='Lawrence')
        user_id = user_to_follow.id
        print(f"Lawrence user id: {user_id}")
        #we now need to follow this user
        self.follow_url = reverse('following',args=[user_id])
        response = self.client.post(self.follow_url)
        print(response.data)
        self.assertEquals(response.status_code,status.HTTP_202_ACCEPTED)
        user_following = User.objects.get(username='Michael')
        following_count = user_following.following.all().count() #It tracks number of followers the user has
        print(f"number of folowers by Michael at the start: {following_count}")
        #we then need to do unfollow
        self.unfollow_url = reverse('unfollow',args=[user_id])
        response = self.client.post(self.unfollow_url)
        print(response.data)
        self.assertEquals(response.status_code,status.HTTP_202_ACCEPTED)
        #we then see whether the follower count has changed
        user_following = User.objects.get(username='Michael')
        following_count = user_following.following.all().count()
        #we print the output
        print(f"number of folowers by Michael after the unfollow: {following_count}")
        #I want to see whether I can see the change in followers after the unfollow or follow inside the user profile
        response = self.client.get(reverse('userprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("follower_count",response.data)
        # self.assertIn("username",response.data["user"])
        self.assertEquals(response.data["follower_count"],0) #we check whether the follower count is zero
    def test_view_users(self):
        #we login in with a specific user
        response = self.client.post(self.login_user_url,{
            "email":"michael@gmail.com",
            "password":"Michael1234.",
        })
        token = response.data.get('token')
        print(f"Token for Michael: {token}")
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        #we test whether we shall see all users
        self.view_users_url = reverse('viewusers')
        response = self.client.get(self.view_users_url)
        print(response.data)
    def test_notification_after_following_user_and_after_reading_notification(self):
        #first we log in the user
        response = self.client.post(self.login_user_url,{
            "email":"michael@gmail.com",
            "password":"Michael1234.",
        })
        # self.client.login(email="michael@gmail.com",password="Michael1234.")
        token = response.data.get('token')
        print(f"Token for Michael: {token}")
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we check whether that login worked
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        #we now need to follow another user
        User = get_user_model()
        user_to_follow = User.objects.get(username='Lawrence')
        user_id = user_to_follow.id
        print(f"Lawrence user id during notification test: {user_id}")
        #we now need to follow this user
        self.follow_url = reverse('following',args=[user_id])
        response = self.client.post(self.follow_url)
        print(response.data)
        self.assertEquals(response.status_code,status.HTTP_202_ACCEPTED)
        user_following = User.objects.get(username='Michael')
        following_count = user_following.following.all().count() #It tracks number of followers the user has
        print(f"number of people Michael is following testing notification: {following_count}")
        self.client.logout()
        #we now login lawrence who has been followed by Michael to check notifications
        self.client.login(email='lawssen@gmail.com',password='Michael1234.')
        #we estbalish logic for checking notifications
        user = get_user_model().objects.get(email='lawssen@gmail.com')
        self.notification_url = reverse('user notifications')
        total_notifications = user.recipient_notifications.all().count()
        print(f'total notifications for Lawrence: {total_notifications}')
        response = self.client.get(self.notification_url)
        print(f'response data for notifications for Lawrence: {response.data}')
        #Filter is seen=False
        self.filter_url = f"{self.notification_url}?is_seen=False" #we should use a string like this
        #We examine the data
        response = self.client.get(self.filter_url)
        print(f"Notifications with is_seen=False before reading: {response.data}")
        #we get lawrence to read notifications
        #trying to print notification data
        notifications = response.data['user notifications']
        print(f'I am trying to see data content for user notifications {notifications}')
        notification_id = notifications[0]['id']
        notification = Notification.objects.get(id=notification_id)
        print(f'notification is seen status before reading {notification.is_seen}')
        print(f'I am then trying to access the id of that notification {notification_id}')
        #here we get the notification id
        self.read_notifications_url = reverse('read notifications',args=[notification_id]) #pass it as an argument
        response = self.client.post(self.read_notifications_url) #get to mark the notification as read
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        notification_id = notifications[0]['id']
        notification = Notification.objects.get(id=notification_id)
        print(f'notification is seen status after reading {notification.is_seen}')
        #I now want to filter so that I see whether the results are none for is_seen =False
        self.filter_url = f"{self.notification_url}?is_seen=False" #we should use a string like this
        response = self.client.get(self.filter_url)
        print(f"Notifications with is_seen=False after reading: {response.data}")