import mysql.connector

class Book:
    def __init__(self, title, author, genre, publication_date, availability=True):
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__publication_date = publication_date
        self.__availability = availability
        self.__borrowed_by = None
        self.__due_date = None

    def title(self):
        return self.__title

    def author(self):
        return self.__author

    def genre(self):
        return self.__genre

    def publication_date(self):
        return self.__publication_date

    def availability(self):
        return self.__availability

    def borrow(self):
        self.__availability = False

    def return_book(self):
        self.__availability = True

    def __borrowed_by(self):
        return self.__borrowed_by

    def __due_date(self):
        return self.__due_date


class User:
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id
        self.__borrowed_books = []
        self.__reserved_books = []
        self.__fines = 0

    def name(self):
        return self.__name

    def library_id(self):
        return self.__library_id

    def borrowed_books(self):
        return self.__borrowed_books

    def borrow_book(self, book_title):
        self.__borrowed_books.append(book_title)

    def return_book(self, book_title):
        self.__borrowed_books.remove(book_title)

    def __reserved_books(self):
        return self.__reserved_books

    def reserve_book(self, book_title):
        self.__reserved_books.append(book_title)

    def __fines(self):
        return self.__fines


class Author:
    def __init__(self, name, biography):
        self.__name = name
        self.__biography = biography

    def name(self):
        return self.__name

    def biography(self):
        return self.__biography


# Database connection settings
username = 'root'
password = 'Ariella21$'
host = '127.0.0.1'

# Create a connection to the database
cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS lms_host")

# Switch to the 'lms_host' database
cursor.execute("USE lms_host")

# Create the database tables
create_tables = [
    """
    CREATE TABLE IF NOT EXISTS authors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        biography TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author_id INT,
        genre VARCHAR(255) NOT NULL,
        publication_date DATE,
        availability BOOLEAN DEFAULT 1,
        FOREIGN KEY (author_id) REFERENCES authors(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        library_id VARCHAR(10) NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS borrowed_books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        book_id INT,
        borrow_date DATE NOT NULL,
        return_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    );
    """
]

for query in create_tables:
    cursor.execute(query)

# Commit the changes and close the cursor and connection
cnx.commit()
cursor.close()
cnx.close()