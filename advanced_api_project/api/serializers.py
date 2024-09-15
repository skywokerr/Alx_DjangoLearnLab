from rest_framework import serializers
from .models import Author,Book
from datetime import datetime
"""Step 4: Create Custom Serializers
Serializer Details:

Create a BookSerializer that serializes all fields of the Book model.
Create an AuthorSerializer that includes:
The name field.
A nested BookSerializer to serialize the related books dynamically.
Validation Requirements:

Add custom validation to the BookSerializer to ensure the publication_year is not in the future.
"""
#I have first created the book serializer.
#I have added the validation and added the year as well so that it is specific to validate the model attribute publication_year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','author','title','publication_year']
    def validate_publication_year(self,value):
        if value > datetime.now().year:
            raise serializers.ValidationError("Year cannot be in the future")
        return value
#I have inherited from the Book serializer through a nested relationship. I then included the books in the fields
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name','books']

