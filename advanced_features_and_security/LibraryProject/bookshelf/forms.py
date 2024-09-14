from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from .models import Book
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
class ExampleForm(forms.Form):
    # Add form fields here
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author','publication_year']


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email','date_of_birth')
User = get_user_model()

# class CustomLoginForm(AuthenticationForm):
#     # email = forms.EmailField(required=True)
#     class Meta:
#         model = User
#         fields = ('email','password')
#     # email = forms.EmailField(required=True)
#     # password = forms.CharField(widget=forms.PasswordInput, required=True)

# class CustomLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         password = cleaned_data.get('password')
#         if email and password:
#             user = authenticate(email=email, password=password)
#             if not user:
#                 raise forms.ValidationError('Invalid email or password')
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = User  # Adjust this if you're using a custom user model
        fields = ['email', 'password']  # Or 'email', 'password' depending on your implementation
