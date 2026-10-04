from datetime import date
from models.book import Book
from models.user import User
from utils.file_handler import load_data, save_data


class Library:
    def __init__(self):
        self.data = load_data()

    def add_book(self, title, author, quantity):
        if not title.strip() or not author.strip():
            raise ValueError("Title and author are required.")

        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        book_ids = [
            book["book_id"] for book in self.data["books"]
        ]

        book_id = max(book_ids, default=0) + 1

        book = Book(book_id, title.strip(), author.strip(), quantity)

        self.data["books"].append(book.to_dict())
        save_data(self.data)

        print("Book added successfully. ID:", book_id)

    def view_books(self):
        books = self.data["books"]

        if not books:
            print("No books found.")
            return

        print("\n--- Available Books ---")

        for item in books:
            book = Book.from_dict(item)

            if book.available > 0:
                print(
                    f"ID: {book.book_id} | "
                    f"Title: {book.title} | "
                    f"Author: {book.author} | "
                    f"Available: {book.available}"
                )

    def search_book(self, keyword):
        keyword = keyword.strip().lower()

        if not keyword:
            raise ValueError("Search keyword cannot be empty.")

        results = []

        for item in self.data["books"]:
            book = Book.from_dict(item)

            if (keyword in book.title.lower()
                    or keyword in book.author.lower()
                    or keyword == str(book.book_id)):
                results.append(book)

        if not results:
            print("No matching books found.")
            return

        for book in results:
            print(
                f"ID: {book.book_id} | "
                f"Title: {book.title} | "
                f"Author: {book.author} | "
                f"Available: {book.available}"
            )

    def register_user(self, name):
        if not name.strip():
            raise ValueError("User name cannot be empty.")

        user_ids = [
            user["user_id"] for user in self.data["users"]
        ]

        user_id = max(user_ids, default=0) + 1
        user = User(user_id, name.strip())

        self.data["users"].append(user.to_dict())
        save_data(self.data)

        print("User registered. ID:", user_id)

    def issue_book(self, book_id, user_id):
        book = self.find_book(book_id)
        user = self.find_user(user_id)

        if book is None:
            raise LookupError("Book not found.")

        if user is None:
            raise LookupError("User not found.")

        if book["available"] <= 0:
            raise ValueError("Book is currently unavailable.")

        book["available"] -= 1

        self.data["issued"].append({
            "book_id": book_id,
            "user_id": user_id,
            "issue_date": str(date.today()),
            "return_date": None
        })

        save_data(self.data)
        print("Book issued successfully.")

    def return_book(self, book_id, user_id):
        book = self.find_book(book_id)

        if book is None:
            raise LookupError("Book not found.")

        for record in self.data["issued"]:
            if (record["book_id"] == book_id
                    and record["user_id"] == user_id
                    and record["return_date"] is None):

                record["return_date"] = str(date.today())
                book["available"] += 1

                save_data(self.data)
                print("Book returned successfully.")
                return

        raise LookupError("No active issue record found.")

    def track_issued_books(self):
        active = [
            record for record in self.data["issued"]
            if record["return_date"] is None
        ]

        if not active:
            print("No books are currently issued.")
            return

        for record in active:
            book = self.find_book(record["book_id"])
            user = self.find_user(record["user_id"])

            print(
                f"Book: {book['title']} | "
                f"User: {user['name']} | "
                f"Issue date: {record['issue_date']}"
            )

    def find_book(self, book_id):
        for book in self.data["books"]:
            if book["book_id"] == book_id:
                return book
        return None

    def find_user(self, user_id):
        for user in self.data["users"]:
            if user["user_id"] == user_id:
                return user
        return None