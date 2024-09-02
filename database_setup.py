import mysql.connector
from mysql.connector import Error
from library_management_sys import Book, User, Author
from datetime import date


# Create a connection to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.01',
            password='Ariella21$',
            database='lms_host'
        )
        return connection
    except Error as e:
        print(f"Error creating connection: {e}")

# Create the database tables
def create_tables(connection):
    cursor = connection.cursor()

    # Create the authors table
    authors_table_query = """
        CREATE TABLE IF NOT EXISTS authors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            biography TEXT
        )
    """
    cursor.execute(authors_table_query)

    # Create the books table
    books_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INT,
            isbn VARCHAR(13) NOT NULL,
            publication_date DATE,
            availability BOOLEAN DEFAULT 1,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )
    """
    cursor.execute(books_table_query)

    # Create the users table
    users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            library_id VARCHAR(10) NOT NULL UNIQUE
        )
    """
    cursor.execute(users_table_query)

    # Create the borrowed_books table
    borrowed_books_table_query = """
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_id INT,
            borrow_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """
    cursor.execute(borrowed_books_table_query)

    connection.commit()

# Main menu
def main_menu():
    print("Welcome to the Library Management System with Database Integration!")
    print("****")
    print("Main Menu:")
    print("1. Book Operations")
    print("2. User Operations")
    print("3. Author Operations")
    print("4. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        book_operations()
    elif choice == "2":
        user_operations()
    elif choice == "3":
        author_operations()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main_menu()

# Book operations
def book_operations():
    print("Book Operations:")
    print("1. Add a new book")
    print("2. Borrow a book")
    print("3. Return a book")
    print("4. Search for a book")
    print("5. Display all books")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        borrow_book()
    elif choice == "3":
        return_book()
    elif choice == "4":
        search_book()
    elif choice == "5":
        display_books()
    else:
        print("Invalid choice. Please try again.")
        book_operations()

# Add a new book
def add_book():
    connection = create_connection()
    cursor = connection.cursor()

    title = input("Enter the book title: ")
    author_name = input("Enter the author name: ")
    isbn = input("Enter the ISBN: ")
    publication_date = input("Enter the publication date (YYYY-MM-DD): ")

    # Get the author ID
    author_query = "SELECT id FROM authors WHERE name = %s"
    cursor.execute(author_query, (author_name,))
    author_id = cursor.fetchone()

    if author_id is None:
        # Add the author if they don't exist
        add_author_query = "INSERT INTO authors (name) VALUES (%s)"
        cursor.execute(add_author_query, (author_name,))
        author_id = cursor.lastrowid
    else:
        author_id = author_id[0]

    # Add the book
    add_book_query = "INSERT INTO books (title, author_id, isbn, publication_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(add_book_query, (title, author_id, isbn, publication_date))

    connection.commit()
    connection.close()

    print("Book added successfully!")

# Borrow a book
def borrow_book():
    connection = create_connection()
    cursor = connection.cursor()

    book_title = input("Enter the book title: ")
    user_library_id = input("Enter your library ID: ")

    # Get the book ID
    book_query = "SELECT id FROM books WHERE title = %s AND availability = 1"
    cursor.execute(book_query, (book_title,))
    book_id = cursor.fetchone()

    if book_id is None:
        print("The requested book is not available for borrowing.")
    else:
        book_id = book_id[0]

        # Get the user ID
        user_query = "SELECT id FROM users WHERE library_id = %s"
        cursor.execute(user_query, (user_library_id,))
        user_id = cursor.fetchone()

        if user_id is None:
            print("The user with the given library ID does not exist.")
        else:
            user_id = user_id[0]

            # Borrow the book
            borrow_date = date.today()
            borrow_query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, %s)"
            cursor.execute(borrow_query, (user_id, book_id, borrow_date))

            # Update the book's availability
            update_availability_query = "UPDATE books SET availability = 0 WHERE id = %s"
            cursor.execute(update_availability_query, (book_id,))

            connection.commit()
            connection.close()

            print("The book has been successfully borrowed!")

# Return a book
def return_book():
    connection = create_connection()
    cursor = connection.cursor()

    book_title = input("Enter the book title: ")
    user_library_id = input("Enter your library ID: ")

    # Get the book ID
    book_query = "SELECT id FROM books WHERE title = %s AND availability = 0"
    cursor.execute(book_query, (book_title,))
    book_id = cursor.fetchone()

    if book_id is None:
        print("The requested book is not currently borrowed.")
    else:
        book_id = book_id[0]

        # Get the user ID
        user_query = "SELECT id FROM users WHERE library_id = %s"
        cursor.execute(user_query, (user_library_id,))
        user_id = cursor.fetchone()

        if user_id is None:
            print("The user with the given library ID does not exist.")
        else:
            user_id = user_id[0]

            # Return the book
            return_date = date.today()
            return_query = "UPDATE borrowed_books SET return_date = %s WHERE user_id = %s AND book_id = %s"
            cursor.execute(return_query, (return_date, user_id, book_id))

            # Update the book's availability
            update_availability_query = "UPDATE books SET availability = 1 WHERE id = %s"
            cursor.execute(update_availability_query, (book_id,))

            connection.commit()
            connection.close()

            print("The book has been successfully returned!")

# Display all books
def display_books():
    connection = create_connection()
    cursor = connection.cursor()

    select_books_query = "SELECT b.id, b.title, a.name, b.isbn, b.publication_date, b.availability FROM books b JOIN authors a ON b.author_id = a.id"
    cursor.execute(select_books_query)

    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, ISBN: {row[3]}, Publication Date: {row[4]}, Availability: {row[5]}")

    connection.close()

# Search for a book
def search_book():
    search_query = input("Enter the search query: ")

    connection = create_connection()
    cursor = connection.cursor()

    select_books_query = f"SELECT book.id, book.title, author.name book.publication_date, book.availabilty,FROM books b JOIN authors a ON b.author_id = a.id WHERE b.title LIKE '%{search_query}%' OR a.name LIKE '%{search_query}%' OR b.isbn LIKE '%{search_query}%'"
    cursor.execute(select_books_query), (f"{search_query}", f"{search_query}", f"{search_query}") 

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, ISBN: {row[3]}, Publication Date: {row[4]}, Availability: {row[5]}")
    else:
        print("No results found.")

    connection.close()

# User operations
def user_operations():
    print("User Operations:")
    print("1. Add a new user")
    print("2. Delete a user")
    print("3. Update a user's library ID")
    print("4. Display all users")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_user()
    elif choice == "2":
        delete_user()
    elif choice == "3":
        update_user_library_id()
    elif choice == "4":
        display_users()
    else:
        print("Invalid choice. Please try again.")
        user_operations()

# Add a new user
def add_user():
    connection = create_connection()
    cursor = connection.cursor()

    name = input("Enter the user's name: ")
    library_id = input("Enter the user's library ID: ")

    add_user_query = "INSERT INTO users (name, library_id) VALUES (%s, %s)"
    cursor.execute(add_user_query, (name, library_id))

    connection.commit()
    connection.close()

    print("User added successfully!")

# Delete a user
def delete_user():
    connection = create_connection()
    cursor = connection.cursor()

    library_id = input("Enter the user's library ID: ")

    delete_user_query = "DELETE FROM users WHERE library_id = %s"
    cursor.execute(delete_user_query, (library_id,))

    connection.commit()
    connection.close()

    print("User deleted successfully!")

# Update a user's library ID
def update_user_library_id():
    connection = create_connection()
    cursor = connection.cursor()

    library_id = input("Enter the user's current library ID: ")
    new_library_id = input("Enter the user's new library ID: ")

    update_user_query = "UPDATE users SET library_id = %s WHERE library_id = %s"
    cursor.execute(update_user_query, (new_library_id, library_id))

    connection.commit()
    connection.close()

    print("User's library ID updated successfully!")

# Display all users
def display_users():
    connection = create_connection()
    cursor = connection.cursor()

    select_users_query = "SELECT id, name, library_id FROM users"
    cursor.execute(select_users_query)

    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Library ID: {row[2]}")

    connection.close()

# Author operations
def author_operations():
    print("Author Operations:")
    print("1. Add a new author")
    print("2. Delete an author")
    print("3. Update an author's biography")
    print("4. Display all authors")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_author()
    elif choice == "2":
        delete_author()
    elif choice == "3":
        update_author_biography()
    elif choice == "4":
        display_authors()
    else:
        print("Invalid choice. Please try again.")
        author_operations()

# Add a new author
def add_author():
    connection = create_connection()
    cursor = connection.cursor()

    name = input("Enter the author's name: ")
    biography = input("Enter the author's biography: ")

    add_author_query = "INSERT INTO authors (name, biography) VALUES (%s, %s)"
    cursor.execute(add_author_query, (name, biography))

    connection.commit()
    connection.close()

    print("Author added successfully!")

# Delete an author
def delete_author():
    connection = create_connection()
    cursor = connection.cursor()

    name = input("Enter the author's name: ")

    delete_author_query = "DELETE FROM authors WHERE name = %s"
    cursor.execute(delete_author_query, (name,))

    connection.commit()
    connection.close()

    print("Author deleted successfully!")

# Update an author's biography
def update_author_biography():
    connection = create_connection()
    cursor = connection.cursor()

    name = input("Enter the author's name: ")
    new_biography = input("Enter the author's new biography: ")

    update_author_query = "UPDATE authors SET biography = %s WHERE name = %s"    
    cursor.execute(update_author_query, (new_biography, name))

    connection.commit()
    connection.close()

    print("Author's biography updated successfully!")

# Display all authors
def display_authors():
    connection = create_connection()
    cursor = connection.cursor()

    select_authors_query = "SELECT id, name, biography FROM authors"
    cursor.execute(select_authors_query)

    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Biography: {row[2]}")

    connection.close()

# Main menu
def main_menu():
    print("Library Management System")
    print("1. Book Operations")
    print("2. User Operations")
    print("3. Author Operations")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        book_operations()
    elif choice == "2":
        user_operations()
    elif choice == "3":
        author_operations()
    elif choice == "4":
        print("Exiting the system. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main_menu()

# Start the program
main_menu()
                            