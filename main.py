from services.library import Library

def get_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


def main():
    try:
        library = Library()
    except (ValueError, OSError) as error:
        print("Unable to load library:", error)
        return

    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. View Available Books")
        print("3. Search Book")
        print("4. Register User")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Track Issued Books")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                title = input("Enter title: ")
                author = input("Enter author: ")
                quantity = get_integer("Enter quantity: ")

                library.add_book(title, author, quantity)

            elif choice == "2":
                library.view_books()

            elif choice == "3":
                keyword = input("Enter title, author, or ID: ")
                library.search_book(keyword)

            elif choice == "4":
                name = input("Enter user name: ")
                library.register_user(name)

            elif choice == "5":
                book_id = get_integer("Enter book ID: ")
                user_id = get_integer("Enter user ID: ")

                library.issue_book(book_id, user_id)

            elif choice == "6":
                book_id = get_integer("Enter book ID: ")
                user_id = get_integer("Enter user ID: ")

                library.return_book(book_id, user_id)

            elif choice == "7":
                library.track_issued_books()

            elif choice == "0":
                print("Thank you for using the system.")
                break

            else:
                print("Invalid menu choice.")

        except (ValueError, LookupError, OSError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()