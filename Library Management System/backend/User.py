# Note: IDGenerator is a separate utility class
class IDGenerator: 
    """Utility class for generating unique IDs."""
    def __init__(self, prefix='LIB'):
        self.prefix = prefix
        self.current_id = 1000

    def generate_id(self):
        self.current_id += 1
        return f"{self.prefix}{self.current_id}"

class LibraryCard: 
    """Represents a user's library card."""
    def __init__(self, user_id, expiry_days=365):
        self.card_id = IDGenerator(prefix='CARD').generate_id()
        self.user_id = user_id
        self.is_active = True
        self.expiry_days = expiry_days 
    
    def __str__(self):
        status = "Active" if self.is_active else "Expired"
        return f"Card ID: {self.card_id}, Status: {status}"

class User:
    """Base class for all library members."""
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name.strip()
        self.card = LibraryCard(user_id)
        self.borrowed_books = []
        
    def __str__(self):
        return f"User ID: {self.id}, Name: {self.name}, Type: {self.__class__.__name__}"
        
class Patron(User):
    """Represents a regular library member."""
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.max_books_allowed = 5
        
    def can_borrow(self):
        return len(self.borrowed_books) < self.max_books_allowed

class Librarian(User):
    """Represents a staff member with administrative privileges."""
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.is_admin = True