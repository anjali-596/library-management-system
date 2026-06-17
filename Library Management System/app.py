import json
from flask import Flask, render_template, request, redirect, url_for, flash
import io
import sys
import os

# =========================================================================
# 1. CORE OOP INTEGRATION
# Ensures the project root is in path for module discovery (Crucial for package imports)
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from backend.Admin import Admin
    from backend.OperationsManager import OperationsManager
    
    ops_manager = OperationsManager() 
    
except ImportError as e:
    # Fallback/Mock for ImportError (should no longer be needed with __init__.py)
    class MockAdmin:
        def __init__(self): 
            print(f"System Fallback: Backend classes not found. Error: {e}")
        def add_book(self, *args, **kwargs): return "ERROR: System not fully initialized. Check imports."
        def search_for_book(self, query): return "ERROR: System not fully initialized. Check imports."
        def add_user(self, *args, **kwargs): return "ERROR: System not fully initialized. Check imports."
        def borrow_book(self, *args): return "ERROR: System not fully initialized. Check imports."
        def return_book(self, *args): return "ERROR: System not fully initialized. Check imports."
        def print_all_books(self): return "ERROR: System not fully initialized. Check imports."
        def print_users_borrowed(self): return "ERROR: System not fully initialized. Check imports."
        def print_all_users(self): return "ERROR: System not fully initialized. Check imports."
        
    class OperationsManager:
        def __init__(self): self.admin = MockAdmin()

    ops_manager = OperationsManager()

# =========================================================================

app = Flask(__name__)
app.secret_key = os.urandom(24) 

VIEW_OPERATIONS = {
    'all_books': ('print_all_books', '#print-books'),
    'borrowed_users': ('print_users_borrowed', '#print-borrowers'),
    'all_users': ('print_all_users', '#print-all-users'),
}

@app.route('/')
def index():
    target_section = request.args.get('target', request.args.get('view') or "#add-book")
    if target_section and not target_section.startswith('#'):
         target_section = '#' + target_section

    view_action = request.args.get('view')
    console_output = None
    
    if view_action in VIEW_OPERATIONS:
        op_name, anchor = VIEW_OPERATIONS[view_action]
        target_section = anchor 
        
        try:
            op_func = getattr(ops_manager.admin, op_name)
            output = op_func()
            console_output = output
            flash(f"Data retrieved successfully.", 'info')
        except Exception as e:
            console_output = f"SERVER ERROR: Could not perform operation '{op_name}'. Details: {e}"
            flash("An error occurred while fetching data. Check server logs.", 'error')
            
    return render_template('index.html', console_output=console_output) + target_section

@app.route('/handle_form', methods=['POST'])
def handle_form():
    action = request.form.get('action')
    result = None
    target_section = "#add-book"

    try:
        if action == 'add_book':
            book_id = request.form['book_id']
            book_name = request.form['book_name']
            book_quantity = request.form['book_quantity']
            
            # Capture BookDetails and Type fields
            author = request.form.get('author')
            isbn = request.form.get('isbn')
            pub_year = request.form.get('pub_year')
            book_type = request.form.get('book_type', 'Physical')
            
            location = request.form.get('location') if book_type == 'Physical' else None
            
            file_size_raw = request.form.get('file_size')
            
            
            file_size = float(file_size_raw) if file_size_raw and book_type == 'Ebook' else None
            
            result = ops_manager.admin.add_book(
                book_id, book_name, book_quantity, 
                author=author, isbn=isbn, pub_year=pub_year, 
                book_type=book_type, location=location, file_size=file_size
            ) 
            target_section = "#add-book"

        elif action == 'search_books':
            query = request.form['query']
            result = ops_manager.admin.search_for_book(query)
            
            if result.startswith("No book found"):
                flash(result, 'info')
                console_output = result
            else:
                flash("Search results displayed below.", 'success')
                console_output = f"Books found for prefix '{query}':\n{result}"
            
            return render_template('index.html', console_output=console_output) + "#search-books"

        elif action == 'add_user':
            user_id = request.form['user_id']
            user_name = request.form['user_name']
            user_type = request.form.get('user_type', 'Patron')
            
            result = ops_manager.admin.add_user(user_id, user_name, user_type=user_type) 
            target_section = "#add-user"

        elif action == 'borrow_book':
            user_name = request.form['user_name']
            book_name = request.form['book_name']
            result = ops_manager.admin.borrow_book(user_name, book_name)
            target_section = "#borrow-book"

        elif action == 'return_book':
            user_name = request.form['user_name']
            book_name = request.form['book_name']
            result = ops_manager.admin.return_book(user_name, book_name)
            target_section = "#return-book"
            
        else:
            flash("Invalid operation selected.", 'error')
            return redirect(url_for('index', target=target_section))
            
        if result.startswith("SUCCESS"):
            flash(result, 'success')
        elif result.startswith("ERROR"):
            flash(result, 'error')
        else:
            flash(f"Operation completed: {result}", 'info')
            
        return redirect(url_for('index', target=target_section))

    except Exception as e:
        flash(f"A server error occurred: {e}", 'error')
        # Print error to console for debugging
        print(f"Server Error: {e}", file=sys.stderr)
        return redirect(url_for('index', target=target_section))

if __name__ == '__main__':
    # Add a fallback to ensure Python version compatibility
    if sys.version_info < (3, 6):
        print("This application requires Python 3.6 or higher.", file=sys.stderr)
        sys.exit(1)
        
    app.run(debug=True)