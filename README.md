Library Management System
==========================

Overview
--------

This is a simple Library Management System implemented in Python using MySQL as the database. The system allows users to create books, users, and authors, and manage book borrowing and returning.

You can modify these settings as needed to connect to your own database.

Classes
-------

The system consists of four classes: `Book`, `User`, `Author`, and `LibraryManagementSystem`.

### Book

The `Book` class has the following attributes:
* `title`: The title of the book
* `author`: The author of the book
* `genre`: The genre of the book
* `publication_date`: The publication date of the book

### User

The `User` class has the following attributes:
* `name`: The name of the user
* `library_id`: The library ID of the user

### Author

The `Author` class has the following attributes:
* `name`: The name of the author
* `id`: The ID of the author

### LibraryManagementSystem

The `LibraryManagementSystem` class has the following methods:

* `borrow_book`: Borrows a book
* `return_book`: Returns a book
* `search_books`: Searches for books
* `list_users`: Lists all users
* `list_borrowed_books`: Lists all borrowed books for a user

Commands
--------

The following commands are available:


* `python setup.py`: Sets up the database
* `python borrow_book.py <user_id> <book_id>`: Borrows a book
* `python return_book.py <book_id>`: Returns a book
* `python search_books.py <title> <author> <genre>`: Searches for books
* `python list_users.py`: Lists all users
* `python list_borrowed_books.py <user_id>`: Lists all borrowed books for a user


Contributing
------------

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

