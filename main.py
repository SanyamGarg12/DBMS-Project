import mysql.connector 

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="SanyamGarg",
        password="1234567",
        database="bookwallah"
    )

def login():
    conn = get_connection()
    cursor = conn.cursor()

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if email == 'admin' and password == 'admin':
        print("Login successful")
        return ('admin', 'admin')
    query = "SELECT * FROM customer_email WHERE email = %s "
    cursor.execute(query, [email])
    user = cursor.fetchone()
    attepmts = user[3]
    if user is None:
        print("Invalid email")
        return None
    elif attepmts >= 3:
        print("Your account is locked. Please contact the admin.")
        return None
    elif user[2] != password:
        print("Invalid email or password.")
        query = "UPDATE customer_email SET number_of_attempts = %s WHERE email = %s"
        cursor.execute(query, (attepmts+1, email))
        conn.commit()
        return None
    else:
        print("---------------------\n\nLogin successful\n")
    conn.close()
    return user

def view_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM book LIMIT 10")
    books = cursor.fetchall()
    print("------------------------")
    for book in books:
        print(f"Book Name: {book[1]}  \t Author: {book[5]}")
        print(f"  Genre: {book[3]} \t Rating: {book[2]}")
        print(f"  Price: {book[4]}")
        print(f"  Publisher: {book[6]}")
        print("------------------------")
    conn.close()

def place_order(book_id, customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO orders (amount, customer_ref_id, order_date, payment_status) VALUES (%s, %s, CURDATE(), 'Pending')"
    cursor.execute(query, (book_id, customer_id))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    print("Order placed successfully.")
    decrease_book_count(book_id, 1)
    return order_id

def update_order_status(order_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE orders SET payment_status = %s WHERE order_id = %s"
    cursor.execute(query, (status, order_id))
    conn.commit()
    conn.close()
    print("Order status updated successfully.")

def add_tracking_details(order_id, status, courier_name):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO tracking_details (order_ref_id, status, courier_name) VALUES (%s, %s, %s)"
    cursor.execute(query, (order_id, status, courier_name))
    conn.commit()
    conn.close()
    print("Tracking details added successfully.")

def decrease_book_count(book_id, count):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE bookstore_inventory SET book_count = book_count - %s WHERE book_ref_id = %s"
    cursor.execute(query, (count, book_id))
    conn.commit()
    conn.close()
    print("Book count decreased successfully.")

def search_books(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    search_query = input("Enter a search query: ")

    query = "SELECT * FROM Book WHERE book_name LIKE %s"
    cursor.execute(query, ('%' + search_query + '%',))
    books = cursor.fetchall()
    print("------------------------")
    for book in books:
        print(f"Book Name: {book[1]}  \t Author: {book[5]}")
        print(f"  Genre: {book[3]} \t Rating: {book[2]}")
        print(f"  Price: {book[4]}")
        print(f"  Publisher: {book[6]}")
        print("------------------------")
    conn.close()
    print("Enter a number to view the book details or press enter to continue.")
    book = input()
    if book:
        book = books[int(book)]
        print(f"Book Name: {book[1]}  \t Author: {book[5]}")
        print(f"  Genre: {book[3]} \t Rating: {book[2]}")
        print(f"  Price: {book[4]}")
        print(f"  Publisher: {book[6]}")
        print("------------------------")
        print("Do you want to place an order for this book?")
        choice = input("Enter 'yes' to place an order or press enter to continue: ")
        if choice.lower() == 'yes':
            place_order(book[0], user_id)
            print("Order placed successfully.")

def find_by_genre():
    conn = get_connection()
    cursor = conn.cursor()

    genre = input("Enter the genre: ")

    query = "SELECT * FROM book WHERE genre = %s"
    cursor.execute(query, (genre,))
    books = cursor.fetchall()
    print("------------------------")
    for book in books:
        print(f"Book Name: {book[1]}  \t Author: {book[5]}")
        print(f"  Genre: {book[3]} \t Rating: {book[2]}")
        print(f"  Price: {book[4]}")
        print(f"  Publisher: {book[6]}")
        print("------------------------")
    conn.close()

def add_book():
    conn = get_connection()
    cursor = conn.cursor()

    bookid = input("Enter the book ID: ")
    book_name = input("Enter the book name: ")

    while True:
        rating = float(input("Enter the book rating (0-5): "))
        if 0 <= rating <= 5:
            break
        else:
            print("Invalid rating. Please enter a number between 0 and 5.")

    genre = input("Enter the book genre: ")

    while True:
        price = int(input("Enter the book price: "))
        if price >= 0:
            break
        else:
            print("Invalid price. Please enter a positive number.")

    author = input("Enter the book author: ")
    publisher = input("Enter the book publisher: ")

    query = """
    INSERT INTO Book (bookid, book_name, rating, genre, price, author, publisher) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (bookid, book_name, rating, genre, price, author, publisher))
    conn.commit()
    conn.close()
    print("Book added successfully.")


def remove_book():
    conn = get_connection()
    cursor = conn.cursor()

    book_name = input("Enter the book name: ")
    author = input("Enter the author name: ")

    query = "DELETE FROM Book WHERE book_name = %s and author = %s"
    cursor.execute(query, (book_name, author))
    conn.commit()
    conn.close()
    print("Book removed successfully.")
 

def top_rated_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Book ORDER BY rating DESC LIMIT 10")
    books = cursor.fetchall()
    print("------------------------")
    for book in books:
        print(f"Book Name: {book[1]}  \t Author: {book[5]}")
        print(f"  Genre: {book[3]} \t Rating: {book[2]}")
        print(f"  Price: {book[4]}")
        print(f"  Publisher: {book[6]}")
        print("------------------------")
    conn.close()

def main():
    user = login()

    if user is None:
        return

    if user[1] == 'admin':
        while True:
            print("1. Add book")
            print("2. Remove book")
            print("3. Top - Rated Books")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                add_book()
            elif choice == '2':
                remove_book()
            elif choice == '3':
                top_rated_books()
            elif choice == '4':
                break
            else:
                print("Invalid choice")
    else:
        while True:
            print("1. View books")
            print("2. Search books")
            print("3. Find by Genre")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                view_books()
            elif choice == '2':
                search_books(user[0])
            elif choice == '3':
                find_by_genre()
            elif choice == '4':
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    main()
