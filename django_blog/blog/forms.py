from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Post,UserProfile,Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from taggit.forms import TagWidget


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','username','password1', 'password2']
class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','image_url']
class UserDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','username']
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','tags']
        widgets = { 
                   'tags': TagWidget(),
}
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
    def validate_content(self,value):
        if len(value)<20:
            raise ValidationError('the length of the comment cannot be less than 10 characters')
        return value
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
    def validate_content(self,value):
        if len(value)<20:
            raise ValidationError('the length of the comment cannot be less than 10 characters')
        return value