from .models import Book,Librarian,Library,Author

#Query all books by a specific author.
author = Author.objects.get(name=author_name)
Book.objects.filter(author=author)

# List all books in a library.
library_instance = Library.objects.get(name=library_name)
books = library_instance.books.all()

# Retrieve the librarian for a library.
librarian_instance = Librarian.objects.get(library=library_name)  
# librarian = library_instance.librarian