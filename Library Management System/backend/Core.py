from datetime import datetime

class LogEntry:
    """Represents a single event log in the system."""
    def __init__(self, event_type, user_id, book_id, message):
        self.timestamp = datetime.now()
        self.event_type = event_type
        self.user_id = user_id
        self.book_id = book_id
        self.message = message
        
    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.event_type} - User {self.user_id}, Book {self.book_id if self.book_id else 'N/A'}: {self.message}"

class Transaction: 
    """Base class for any operation involving a user and a book."""
    def __init__(self, user, book):
        self.user = user
        self.book = book
        self.transaction_date = datetime.now()
        
    def process(self):
        raise NotImplementedError("Subclass must implement abstract method")

class BorrowTransaction(Transaction): 
    """Represents a book borrowing event."""
    def process(self):
        pass

class ReturnTransaction(Transaction): 
    """Represents a book return event."""
    def process(self):
        pass