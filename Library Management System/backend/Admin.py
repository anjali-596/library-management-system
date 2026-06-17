from .Book import Book, SearchService, ReportGenerator, BookDetails, PhysicalBook, Ebook
from .User import User, Patron, Librarian, IDGenerator
from .Core import LogEntry, BorrowTransaction, ReturnTransaction

class Admin:
    """
    Manages the core data and logic. 
    """
    def __init__( self ):
        self.books = []  
        self.users = {}  
        self.transactions = [] 
        self.logs = [] 
        self.user_id_generator = IDGenerator(prefix='U')
        self.book_id_generator = IDGenerator(prefix='B')
        
        self.search_service = SearchService(self.books)
        self.report_generator = ReportGenerator()
        
        # Initial data for demonstration
        self.add_user(self.user_id_generator.generate_id(), 'Alice', user_type='Librarian')
        self.add_user(self.user_id_generator.generate_id(), 'Bob', user_type='Patron')
        self.add_book(self.book_id_generator.generate_id(), 'The Great Gatsby', 5, 'F. Scott Fitzgerald', '9780743273565', 1925, book_type='Physical', location='A1')
        self.add_book(self.book_id_generator.generate_id(), '1984', 2, 'George Orwell', '9780451524935', 1949, book_type='Ebook', file_size=1.5)
        self.log_event("SYSTEM", "INIT", "System initialized with base data.")

    def log_event(self, event_type, user_id, message, book_id=None):
        self.logs.append(LogEntry(event_type, user_id, book_id, message))

    # FIXED: Added all new detailed parameters
    def add_book( self , book_id , book_name , book_quantity , author='Unknown', isbn='N/A', pub_year='N/A', book_type='Physical', location=None, file_size=None):
        try:
            # Type checking and cleanup
            book_quantity = int(book_quantity)
            pub_year = int(pub_year) if pub_year and str(pub_year).isdigit() else 'N/A'
            
            if any(book.id == book_id for book in self.books):
                self.log_event("ERROR", "ADMIN", f"Book with ID {book_id} already exists.", book_id)
                return f"ERROR: Book with ID {book_id} already exists."

            if book_type == 'Physical' and location:
                new_book = PhysicalBook(book_id, book_name, book_quantity, location, author=author, isbn=isbn, pub_year=pub_year)
            elif book_type == 'Ebook' and file_size:
                 new_book = Ebook(book_id, book_name, book_quantity, file_size, author=author, isbn=isbn, pub_year=pub_year)
            else:
                 # Fallback to base Book if type is unknown or details are missing
                 new_book = Book(book_id, book_name, book_quantity, author=author, isbn=isbn, pub_year=pub_year)

            self.books.append(new_book)
            self.log_event("SUCCESS", "ADMIN", f"Book '{book_name}' added successfully.", book_id)
            return f"SUCCESS: Book '{book_name}' added successfully as {book_type}."
        except ValueError:
            self.log_event("ERROR", "ADMIN", "Book quantity or year must be a valid number.")
            return "ERROR: Book quantity or year must be a valid number."

    def print_all_books( self ):
        # Uses enhanced report method from Book.py
        return self.report_generator.generate_all_books_report(self.books)

    def search_for_book( self , query ):
        results = self.search_service.search_by_prefix(query)
        if not results:
             return f"No book found with prefix '{query}'"
        return ", ".join(results)

    # FIXED: Added new user_type parameter
    def add_user( self , user_id , user_name , user_type='Patron'):
        if user_id in self.users:
            self.log_event("ERROR", "ADMIN", f"User ID {user_id} already exists.")
            return f"ERROR: User with ID {user_id} already exists."
        
        if user_type == 'Librarian':
            new_user = Librarian(user_id, user_name)
        else:
            new_user = Patron(user_id, user_name)
            
        self.users[user_id] = new_user
        self.log_event("SUCCESS", "ADMIN", f"User '{user_name}' added successfully.", user_id)
        return f"SUCCESS: User '{user_name}' added successfully as a {user_type}."

    def _find_user_by_name(self, user_name):
        return next((user for user in self.users.values() if user.name.lower() == user_name.lower()), None)

    def _find_book_by_name(self, book_name):
        return next((book for book in self.books if book.name.lower() == book_name.lower()), None)
    
    def borrow_book( self , user_name , book_name ):
        user = self._find_user_by_name(user_name)
        book = self._find_book_by_name(book_name)
        
        if not user: return f"ERROR: User '{user_name}' not found."
        if not book: return f"ERROR: Book '{book_name}' not found in library."
        if book.available_quantity <= 0: return f"ERROR: Book '{book_name}' is currently out of stock."
        if book.name in user.borrowed_books: return f"ERROR: User '{user_name}' has already borrowed '{book_name}'."
        if isinstance(user, Patron) and not user.can_borrow():
            return f"ERROR: Patron '{user_name}' has reached their maximum borrow limit of {user.max_books_allowed}."

        transaction = BorrowTransaction(user, book)
        self.transactions.append(transaction)
        
        book.available_quantity -= 1
        user.borrowed_books.append(book.name)
        
        self.log_event("BORROW", user.id, f"Borrowed '{book_name}'", book.id)
        return f"SUCCESS: '{book_name}' borrowed by {user_name}. {book.available_quantity} copies remaining."

    def return_book( self , user_name , book_name ):
        user = self._find_user_by_name(user_name)
        book = self._find_book_by_name(book_name)
        
        if not user: return f"ERROR: User '{user_name}' not found."
        if not book: return f"ERROR: Book '{book_name}' not found in library."
        if book.name not in user.borrowed_books: return f"ERROR: User '{user_name}' did not borrow '{book_name}'."

        transaction = ReturnTransaction(user, book)
        self.transactions.append(transaction)
            
        book.available_quantity += 1
        user.borrowed_books.remove(book.name)
        
        self.log_event("RETURN", user.id, f"Returned '{book_name}'", book.id)
        return f"SUCCESS: '{book_name}' returned by {user_name}. {book.available_quantity} copies now available."

    def print_users_borrowed( self ):
        # Uses enhanced reporting logic
        borrowers = [u for u in self.users.values() if u.borrowed_books]
        output = "--- USERS CURRENTLY BORROWING BOOKS ---\n"
        
        if not borrowers:
            return output + "No users currently have books borrowed."
            
        report_lines = []
        for u in borrowers:
            type_name = u.__class__.__name__
            report_lines.append(f"{u.name} (ID: {u.id}) - Type: {type_name}")
            report_lines.append(f"  - Borrowed: {', '.join(u.borrowed_books)}")
        
        return output + "\n" + "\n".join(report_lines)
    
    def print_all_users( self ):
        # Uses enhanced report method from Book.py
        return self.report_generator.generate_all_users_report(self.users)