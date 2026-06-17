# backend/Book.py

# required by ReportGenerator to check user types.
from .User import Patron, Librarian # Patron is now defined!

class BookDetails: 
    """Holds non-inventory-specific details about a book."""
    def __init__(self, author, isbn, publication_year):
        self.author = author
        self.isbn = isbn
        # Ensure year is a string if not an integer
        self.publication_year = str(publication_year) 
    
    def __str__(self):
        return f"Author: {self.author}, ISBN: {self.isbn}, Year: {self.publication_year}"

class Book: 
    """Base class for all book types."""
    def __init__(self, book_id, name, quantity, author='Unknown', isbn='N/A', pub_year='N/A'):
        self.id = book_id
        self.name = name
        self.total_quantity = int(quantity)
        self.available_quantity = int(quantity)
        self.details = BookDetails(author, isbn, pub_year)
        
    def __str__(self):
        return f"ID: {self.id}, Title: {self.name}, Total: {self.total_quantity}, Available: {self.available_quantity}"

class PhysicalBook(Book):
    """Represents a physical copy of a book."""
    def __init__(self, book_id, name, quantity, shelf_location='A0', **kwargs):
        
        author = kwargs.pop('author', 'Unknown')
        isbn = kwargs.pop('isbn', 'N/A')
        pub_year = kwargs.pop('pub_year', 'N/A')
        
        # Call superclass with the named arguments it explicitly expects
        super().__init__(book_id, name, quantity, author=author, isbn=isbn, pub_year=pub_year)
        
        self.shelf_location = shelf_location
        self.is_loanable = True

class Ebook(Book):
    """Represents an electronic version of a book."""
    def __init__(self, book_id, name, quantity, file_size_mb=None, **kwargs):
        
        author = kwargs.pop('author', 'Unknown')
        isbn = kwargs.pop('isbn', 'N/A')
        pub_year = kwargs.pop('pub_year', 'N/A')
        
        # Call superclass with the named arguments it explicitly expects
        super().__init__(book_id, name, quantity, author=author, isbn=isbn, pub_year=pub_year)
        
        # 1. Start with a safe default
        self.file_size_mb = 0.0
        
        # 2. Attempt conversion only if a value was provided
        if file_size_mb is not None and file_size_mb != '':
             try:
                 # Try to convert whatever was passed (float, int, or string representation)
                 self.file_size_mb = float(file_size_mb)
             except (TypeError, ValueError):
                 # If conversion fails (e.g., non-numeric string), keep the 0.0 default
                 pass 
            
        self.is_loanable = False

class SearchService: 
    """Handles searching operations for books."""
    def __init__(self, books):
        self.books = books
        
    def search_by_prefix(self, query):
        found_books = [book.name for book in self.books if book.name.upper().startswith(query.upper())]
        return found_books

class ReportGenerator: 
    """Handles generating formatted reports."""
    def generate_all_books_report(self, books):
        output = "--- ALL BOOKS IN LIBRARY ---\n"
        if not books:
            return output + "The library currently holds no books."
        sorted_books = sorted(books, key=lambda b: b.name)
        
        report_lines = []
        for book in sorted_books:
            details = book.details
            
            if isinstance(book, PhysicalBook):
                type_info = f"Type: Physical, Location: {book.shelf_location}"
            elif isinstance(book, Ebook):
                type_info = f"Type: Ebook, File Size: {book.file_size_mb} MB"
            else:
                type_info = "Type: Base"

            report_lines.append(f"{book.name} (ID: {book.id}) - Available: {book.available_quantity}/{book.total_quantity}")
            report_lines.append(f"  - Author: {details.author} | ISBN: {details.isbn} | Year: {details.publication_year}")
            report_lines.append(f"  - {type_info}")
        
        return output + "\n" + "\n".join(report_lines)

    def generate_all_users_report(self, users):
        output = "--- ALL REGISTERED USERS ---\n"
        if not users:
            return output + "No users are currently registered."
        sorted_users = sorted(users.values(), key=lambda u: u.name)
        
        report_lines = []
        for user in sorted_users:
            type_name = user.__class__.__name__
            borrow_info = ""
            # Patron is now correctly defined due to the import at the top
            if isinstance(user, Patron):
                 borrow_info = f", Limit: {user.max_books_allowed}"

            report_lines.append(f"{user.name} (ID: {user.id}) - Type: {type_name}, Card ID: {user.card.card_id}{borrow_info}")
            report_lines.append(f"  - Borrowed Books: {', '.join(user.borrowed_books) or 'None'}")
            
        return output + "\n" + "\n".join(report_lines)