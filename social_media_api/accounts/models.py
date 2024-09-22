from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
#Create a custom user model that extends Django’s AbstractUser,\
    # adding fields such as bio, profile_picture,\
        # and followers (a ManyToMany field referencing itself, symmetrical=False).
class UserManager(BaseUserManager):
    def create_user(self,username,password,email,first_name,last_name,date_of_birth):
        if not email:
            raise ValueError('provide a valid email')
        if not username:
            raise ValueError('provide username')
        if not first_name:
            raise ValueError('provide first_name')
        if not last_name:
            raise ValueError('provide last_name')
        if not date_of_birth:
            raise ValueError('provide date of birth')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,password,email,first_name,last_name,date_of_birth):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='User Email',max_length=100,unique=True,null=False)
    username = models.CharField(verbose_name='Username',unique=True,null=False,max_length=50)
    first_name = models.CharField(verbose_name='first_name',unique=False,null=False,max_length=100)
    last_name = models.CharField(verbose_name='last_name',unique=False,null=False,max_length=100)
    date_of_birth = models.DateField(verbose_name='date of birth')
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.URLField(max_length=255,blank=True,null=True,default=None)
    # profile_picture = models.ImageField(max_length=255,blank=True,null=True,default=None)
    bio = models.TextField(blank=True,null=True,default=None)
    followers = models.ManyToManyField('self',symmetrical=False, blank=True,related_name='following', default=0)
    @property
    def followerscount(self):
        follower_count = self.following.all().count()
        return str(follower_count)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
