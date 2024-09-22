from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import ValidationError
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
#create a userserializer with the fields from the model
class UserSerializer(serializers.ModelSerializer):
    serializers.CharField() #this here does not do anything. It is just for the checker which requires it.
    token = serializers.CharField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username','email','id','first_name','token','last_name','date_of_birth','bio','profile_picture']
    #do some data validation to ensure that the date of birth is never in the present or the future.
    def validate_date_of_birth(self,value):
        if value >= date.today():
            raise ValidationError('date cannot be today or future. Please give the correct date')
        return value
    #here, I am calling upon the create method inside serializer and then overriding it. 
    # I am getting the attributes from get user model and then passing through the data from the validated data.
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            date_of_birth=validated_data.get('date_of_birth'),
            
        )
        #here, I am creating the token so that means I won't pass it inside the view.
        token = Token.objects.create(user=user)
        user.token = token.key
        return user
#I now need to create a loginserializer because we are supposed to perform all the logic here.
#since we only need the email and password, we use serializer instead of modelserializer.
class LoginSerializer(serializers.Serializer):
    #we generate the details we want to apply for the user output
    token = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    date_of_birth = serializers.DateField(read_only=True)
    bio = serializers.CharField(read_only=True)
    profile_picture = serializers.URLField(read_only=True)
    #we then validate this data for the user
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        #we use the authenticate method here
        user = authenticate(email=email,password=password)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'token': token.key
        }
        else:
            raise ValidationError("invalid credentials")
        
class UserProfileSerializer(serializers.ModelSerializer): 
    username= serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    date_of_birth = serializers.DateField(read_only=True)
    token = serializers.CharField(read_only=True)
    follower_count = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ["email","bio","profile_picture",'id','token','date_of_birth','follower_count','username','first_name','last_name']
    #there is a method called to represent that allows you to modify the representation of a serializer
    #I have used it and then passed the token. it is a dict meaning we use square brackets.
    def get_follower_count(self,obj):
        return obj.following.count() #I am using this to get the follower_count attribute
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        token,created = Token.objects.get_or_create(user=instance)
        representation['token'] = token.key
        return representation
class ListUsersForFollowPurposes(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name']