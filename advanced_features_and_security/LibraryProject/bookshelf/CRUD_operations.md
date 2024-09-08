rom bookshelf.models import Book

create

book = Book(title="1984", author = "George Orwell", publication_year = 1949) book.save() book saved successfully

retrieve

Book.objects.all()

output <QuerySet [<Book: Title: Nineteen Eighty-Four Author: George Orwell Publication Year: 1949>]>

update

book = Book.objects.get(title="1984") book.title = "Nineteen Eighty-Four" book.save() book title updated successfully.

delete

book = Book.objects.get(title="Nineteen Eighty-Four") book.delete() output = (1, {'bookshelf.Book': 1})

confirmation output output = <QuerySet []>