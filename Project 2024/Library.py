import json

FILE_PATH = "library.json"
#Import dictionary
library = {
    "books": [],
    "authors": {},
    "publishers": {}
}
#Define counter for the books
book_counter = 1

#Load library from a JSON file and generate new file if there is no library.#
def load_library():
    global library, book_counter
    try:
        with open(FILE_PATH, "r") as file:
            library = json.load(file)
            if library["books"]:
                book_counter = max(book["number"] for book in library["books"]) + 1
    except FileNotFoundError:
        print("No existing library file found. Starting with an empty library.")
    except json.JSONDecodeError:
        print("Error reading the library file. Starting with an empty library.")

#Save the data in the library.#
def save_library():
    with open(FILE_PATH, "w") as file:
        json.dump(library, file, indent=4)
    print("Library data saved successfully.")

#Add a new book to the library with book_counter and without keyboard simbols#
def add_book():
    global book_counter
    while True:
        title = input("(0. exit)\nInsert a title: ").strip()
        if title == "0":
            return
        if not title:
            print("The title is empty. Try again.")
            continue
        while True:
            author = input("Insert author of the book: ").strip()
            if author == "0":
                return
            if author.replace(" ", "").isalpha():  # Allows letters and spaces
                break
            print("Author name not valid. Try again.")
        while True:
            publisher = input("Insert the publisher of the book: ").strip()
            if publisher == "0":
                return
            if publisher.replace(" ", "").isalpha():  # Allows letters and spaces
                break
            print("Publisher name not valid. Try again.")

        if author not in library["authors"]:
            library["authors"][author] = len(library["authors"]) + 1

        if publisher not in library["publishers"]:
            library["publishers"][publisher] = len(library["publishers"]) + 1

        author_id = library["authors"][author]
        publisher_id = library["publishers"][publisher]

        if any(
            book["title"].lower() == title.lower()
            and book["author_id"] == author_id
            and book["publisher_id"] == publisher_id
            for book in library["books"] #Find duplicate system with title, author_id and publisher_id#
        ):
            print(f"The book '{title}' by {author}, published by {publisher}, already exists.")
            return

        new_book = { #Generate a new book and put in status in stock and add a new book counter and option for add another book#
            "number": book_counter,
            "title": title,
            "author_id": author_id,
            "publisher_id": publisher_id,
            "status": "in stock"
        }
        library["books"].append(new_book)
        book_counter += 1
        print(f"The book '{title}' was successfully added!")

        if input("Do you want to add another book? (yes to continue): ").strip().lower() != "yes":
            return

#Display books and option to see book "in stock" or both include "out of stock" books#
def show_books():
    all_books = input("Include out-of-stock books? (yes/no): ").strip().lower() == "yes"

    in_stock = [book for book in library["books"] if book.get("status") == "in stock"]
    out_of_stock_books = [book for book in library["books"] if book.get("status") == "out of stock"]

    in_stock = sorted(in_stock, key=lambda book: book["title"])
    out_of_stock_books = sorted(out_of_stock_books, key=lambda book: book["title"])

    print("\n--- In Stock Books ---")
    if in_stock:
        for book in in_stock:
            author = next((name for name in library["authors"] if library["authors"][name] == book["author_id"]),
                          "Unknown")
            publisher = next(
                (name for name in library["publishers"] if library["publishers"][name] == book["publisher_id"]),
                "Unknown")
            print(f"TITLE: {book['title']}, AUTHOR: {author}, PUBLISHER: {publisher}")
    else:
        print("No books in stock.")

    if all_books:
        print("\n--- Out of Stock Books ---")
        if out_of_stock_books:
            for book in out_of_stock_books:
                author = next((name for name in library["authors"] if library["authors"][name] == book["author_id"]),
                              "Unknown")
                publisher = next(
                    (name for name in library["publishers"] if library["publishers"][name] == book["publisher_id"]),
                    "Unknown")
                print(f"TITLE: {book['title']}, AUTHOR: {author}, PUBLISHER: {publisher}")
        else:
            print("No books out of stock.")

#Search book options for find the book with title, author or publisher and also an option to include "out of stock" books
def search_book():
    print("\nSearch by:")
    print("1. Title")
    print("2. Author")
    print("3. Publisher")
    choice = input("Choose an option (0 to exit): ").strip()

    if choice == "0":
        return

    include_out_of_stock = input("Include out-of-stock books? (yes/no): ").strip().lower() == "yes"

    results = []
    if choice == "1":
        search_key = input("Enter the book title: ").strip().lower()
        for book in library["books"]:
            if book.get("title", "").lower() == search_key:
                if include_out_of_stock or book.get("status") == "in stock":
                    results.append(book)
    elif choice == "2":
        search_key = input("Enter the author name: ").strip()
        author_id = library["authors"].get(search_key)
        for book in library["books"]:
            if book.get("author_id") == author_id:
                if include_out_of_stock or book.get("status") == "in stock":
                    results.append(book)
    elif choice == "3":
        search_key = input("Enter the publisher name: ").strip()
        publisher_id = library["publishers"].get(search_key)
        for book in library["books"]:
            if book.get("publisher_id") == publisher_id:
                if include_out_of_stock or book.get("status") == "in stock":
                    results.append(book)
    else:
        print("Invalid option. Returning to the dashboard.")
        return

    if results:
        print("\nSearch results:")
        for idx, book in enumerate(results, start=1):
            author = next((name for name in library["authors"] if library["authors"][name] == book["author_id"]), "Unknown")
            publisher = next((name for name in library["publishers"] if library["publishers"][name] == book["publisher_id"]), "Unknown")
            status = book.get("status", "in stock")
            print(f"{idx}. Title: {book['title']}, Author: {author}, Publisher: {publisher}, Status: {status}")
    else:
        print(f"No books found for your search.")

#Option to search and remove the books and also you can choose if delete it or put in "out of stock"#
def remove_book():
    print("\nSearch by:")
    print("1. Title")
    print("2. Author")
    print("3. Publisher")
    print("4. All books")
    choice = input("Choose an option (0 to exit): ").strip()

    if choice == "0":
        return
#give numbers for a search key#
    results = []
    if choice == "4":
        results = library["books"]
    elif choice in ["1", "2", "3"]:
        search_key = input("Enter name:").strip().lower()
        for book in library["books"]:
            if choice == "1" and book.get("title", "").lower() == search_key:
                results.append(book)
            elif choice == "2" and library["authors"].get(search_key) == book.get("author_id"):
                results.append(book)
            elif choice == "3" and library["publishers"].get(search_key) == book.get("publisher_id"):
                results.append(book)
    else:
        print("Invalid option. Returning to the dashboard.")
        return
#Show the books matched and will numerate the books in order
    if results:
        print("\nBooks matching your search:")
        for idx, book in enumerate(results, start=1):
            author = next((name for name, id in library["authors"].items() if id == book.get("author_id")), "Unknown")
            publisher = next((name for name, id in library["publishers"].items() if id == book.get("publisher_id")), "Unknown")
            status = book.get("status", "in stock")
            print(f"{idx}. Title: {book['title']}, Author: {author}, Publisher: {publisher}, Status: {status}")

        selection = input("\nEnter the numbers of the books to process (0 to exit, '-' for range, ',' to separate): ").strip()
        if selection == "0":
            print("Cancelled. Returning to the dashboard.")
            return
#Possibility to split the selection book number or give a range if you want chose more books in the same time
        try:
            numbers = set()
            for part in selection.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    numbers.update(range(start, end + 1))
                else:
                    numbers.add(int(part))

            valid_numbers = {n for n in numbers if 1 <= n <= len(results)}
            if not valid_numbers:
                print("No valid numbers selected. Try again.")
                return
#Option to chose if delete permanently or put out of stock
            for num in sorted(valid_numbers, reverse=True):
                book = results[num - 1]
                action = input(f"\nWhat do you want to do with '{book['title']}'?\n1. Mark as 'out of stock'\n2. Permanently delete\nChoose an option (0 to skip): ").strip()
                if action == "1":
                    book["status"] = "out of stock"
                    print(f"Marked as 'out of stock': {book['title']}")
                elif action == "2":
                    confirm = input(f"Are you sure you want to permanently delete '{book['title']}'? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        library["books"].remove(book)
                        print(f"Deleted permanently: {book['title']}")
                    else:
                        print(f"Skipped deletion of: {book['title']}")
                elif action == "0":
                    print(f"Skipped: {book['title']}")
                else:
                    print(f"Invalid action for: {book['title']}. Skipping.")

            print("Processing complete.")
        except ValueError:
            print("Invalid input format. Use numbers separated by ',' or a range with '-'.")
    else:
        print("No books found.")

#Option to convert the books in "out of stock" to "in stock"
def restore_book():
    out_of_stock = [book for book in library["books"] if book.get("status") == "out of stock"]
    if out_of_stock:
        print("\nOut of Stock Books:")
        #numerate the books to chose in order for select which book we want restore
        for idx, book in enumerate(out_of_stock, start=1):
            author = next((name for name in library["authors"] if library["authors"][name] == book["author_id"]), "Unknown")
            publisher = next((name for name in library["publishers"] if library["publishers"][name] == book["publisher_id"]), "Unknown")
            print(f"{idx}. Title: {book['title']}, Author: {author}, Publisher: {publisher}")

        selection = input("\nEnter the numbers of the books to restore (0 to exit, '-' for range, ',' to separate): ").strip()
        if selection == "0":
            print("Cancelled. Returning to the dashboard.")
            return

        try:
            numbers = set()
            for part in selection.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    numbers.update(range(start, end + 1))
                else:
                    numbers.add(int(part))
#Validation of numbers
            valid_numbers = {n for n in numbers if 1 <= n <= len(out_of_stock)}
            if not valid_numbers:
                print("No valid numbers selected. Try again.")
                return

            for num in sorted(valid_numbers):
                book_to_restore = out_of_stock[num - 1]
                book_to_restore["status"] = "in stock"
                print(f"Restored: {book_to_restore['title']}")

            print("Books were successfully restored to 'in stock.'")
        except ValueError:
            print("Invalid input format. Use numbers separated by ',' or a range with '-'.")
    else:
        print("\nNo books out of stock.")

#This is the dashboard with all "def" I created
def main():
    load_library()
    while True:
        print("\n--- The Great Hartland Community Library ---")
        print("1. Add a new book")
        print("2. Show book list")
        print("3. Search a book")
        print("4. Remove a book")
        print("5. Restock books")
        print("6. Exit")

        choice = input("Choose an option: ").strip()
#Assign a number fpr every option
        if choice == "1":
            add_book()
        elif choice == "2":
            show_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            remove_book()
        elif choice == "5":
            restore_book()
        elif choice == "6":
            save_library()
            print("Software closed. Goodbye!")
            break
        else:
            print("Option not valid. Try again.")

if __name__ == "__main__":
    main()
