from flask import Flask, render_template, redirect, url_for, session, request, flash
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for session

# Add a helper function for DB connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Set your MySQL password if you have one
        database="library_db"  # Change to your actual database name
    )

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('library'))
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('signup.html')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            flash('Username already exists!')
            cursor.close()
            conn.close()
            return render_template('signup.html')
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form.get('user_type', 'user')
        conn = get_db_connection()
        cursor = conn.cursor()
        if user_type == 'user':
            cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user and check_password_hash(user[0], password):
                session['logged_in'] = True
                session['username'] = username
                session['user_type'] = 'user'
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!')
        elif user_type == 'admin':
            cursor.execute('SELECT password_hash FROM admins WHERE username = %s', (username,))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()
            if admin and check_password_hash(admin[0], password):
                session['logged_in'] = True
                session['username'] = username
                session['user_type'] = 'admin'
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/loginadmin')
def loginadmin():
    return render_template('loginadmin.html')

# Simulate login for demonstration (no real authentication)
@app.route('/do_login')
def do_login():
    session['logged_in'] = True
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Get user's collections
    cursor.execute('''
        SELECT c.*, COUNT(cb.book_id) as book_count 
        FROM collections c 
        LEFT JOIN collection_books cb ON c.id = cb.collection_id 
        WHERE c.user_id = (SELECT id FROM users WHERE username = %s) 
        GROUP BY c.id
    ''', (session['username'],))
    collections = cursor.fetchall()
    # Get all books from all collections for this user
    books = []
    if collections:
        cursor.execute('''
            SELECT DISTINCT b.*, c.name as collection_name 
            FROM books b 
            JOIN collection_books cb ON b.id = cb.book_id 
            JOIN collections c ON cb.collection_id = c.id 
            WHERE c.user_id = (SELECT id FROM users WHERE username = %s)
            ORDER BY b.title
        ''', (session['username'],))
        books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('Home Page - Lib.html', collections=collections, books=books)

@app.route('/library')
def library():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'az')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the base query
    query = '''
        SELECT c.*, COUNT(cb.book_id) as book_count 
        FROM collections c 
        LEFT JOIN collection_books cb ON c.id = cb.collection_id 
        WHERE c.user_id = (SELECT id FROM users WHERE username = %s)
    '''
    params = [session['username']]

    # Add search filter
    if search:
        query += " AND LOWER(c.name) LIKE %s"
        params.append(f"%{search.lower()}%")

    query += " GROUP BY c.id"

    # Add sort
    if sort == 'za':
        query += " ORDER BY c.name DESC"
    else:
        query += " ORDER BY c.name ASC"

    cursor.execute(query, params)
    collections = cursor.fetchall()

    # Get all books from all collections for this user
    books = []
    if collections:
        cursor.execute('''
            SELECT DISTINCT b.*, c.name as collection_name 
            FROM books b 
            JOIN collection_books cb ON b.id = cb.book_id 
            JOIN collections c ON cb.collection_id = c.id 
            WHERE c.user_id = (SELECT id FROM users WHERE username = %s)
            ORDER BY b.title
        ''', (session['username'],))
        books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('Home Page - Lib.html', 
                         collections=collections,
                         books=books)

@app.route('/add_items', methods=['GET', 'POST'])
def add_items():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    search = request.values.get('search', '').strip()
    sort = request.values.get('sort', 'az')
    message = None
    search_results = None
    selected_collection = None
    collection_id = request.values.get('collection_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user's collections
    cursor.execute('''
        SELECT c.* 
        FROM collections c 
        WHERE c.user_id = (SELECT id FROM users WHERE username = %s)
        ORDER BY c.name
    ''', (session['username'],))
    collections = cursor.fetchall()

    # Handle add-to-collection POST
    if request.method == 'POST' and request.form.get('add_book_id'):
        collection_id = request.form.get('collection_id')
        add_book_id = request.form.get('add_book_id')
        if collection_id and add_book_id:
            cursor.execute('SELECT * FROM books WHERE id = %s', (add_book_id,))
            book = cursor.fetchone()
            if book:
                cursor.execute('SELECT * FROM collection_books WHERE collection_id = %s AND book_id = %s', (collection_id, book['id']))
                if not cursor.fetchone():
                    cursor.execute('INSERT INTO collection_books (collection_id, book_id) VALUES (%s, %s)', (collection_id, book['id']))
                    conn.commit()
                    message = f"Book '{book['title']}' added to collection!"
                else:
                    message = f"Book '{book['title']}' is already in this collection."
            selected_collection = int(collection_id)

    # Handle search (GET or POST)
    if (request.method == 'POST' and request.form.get('search_query')) or (request.method == 'GET' and search):
        search_query = request.values.get('search_query', search)
        search_type = request.values.get('search_type', 'keyword')
        if search_type == 'isbn':
            cursor.execute('SELECT * FROM books WHERE isbn = %s', (search_query,))
            book = cursor.fetchone()
            search_results = [book] if book else []
        else:
            cursor.execute('''
                SELECT * FROM books 
                WHERE LOWER(title) LIKE %s 
                OR LOWER(author) LIKE %s 
                OR LOWER(genre) LIKE %s
            ''', (f'%{search_query.lower()}%', f'%{search_query.lower()}%', f'%{search_query.lower()}%'))
            search_results = cursor.fetchall()
        if not search_results:
            message = "No books found matching your search."

    cursor.close()
    conn.close()

    return render_template('add_items.html',
                         collections=collections,
                         message=message,
                         search_results=search_results,
                         selected_collection=selected_collection)

@app.route('/add_collection', methods=['GET', 'POST'])
def add_collection():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # --- Search and filter logic for GET requests ---
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'az')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the base query
    query = '''
        SELECT c.*, COUNT(cb.book_id) as book_count 
        FROM collections c 
        LEFT JOIN collection_books cb ON c.id = cb.collection_id 
        WHERE c.user_id = (SELECT id FROM users WHERE username = %s)
    '''
    params = [session['username']]

    # Add search filter
    if search:
        query += " AND LOWER(c.name) LIKE %s"
        params.append(f"%{search.lower()}%")

    query += " GROUP BY c.id"

    # Add sort
    if sort == 'za':
        query += " ORDER BY c.name DESC"
    else:
        query += " ORDER BY c.name ASC"

    cursor.execute(query, params)
    collections = cursor.fetchall()

    # --- Handle POST for adding a new collection ---
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        language = request.form.get('language', 'en')  # Get language from form

        if not collection_name:
            flash('Collection name is required!')
            cursor.close()
            conn.close()
            return render_template('add_collection.html', collections=collections)

        # Get user_id from username in session
        cursor.execute('SELECT id FROM users WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if not user:
            flash('User not found!')
            cursor.close()
            conn.close()
            return render_template('add_collection.html', collections=collections)

        user_id = user['id']
        cursor.execute('INSERT INTO collections (name, user_id, language) VALUES (%s, %s, %s)', 
                      (collection_name, user_id, language))
        conn.commit()
        flash('Collection added successfully!')
        # Refresh collections after adding
        cursor.execute(query, params)
        collections = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('add_collection.html', collections=collections)

@app.route('/add_items_click', methods=['GET', 'POST'])
def add_items_click():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user's collections
    cursor.execute('''
        SELECT c.* 
        FROM collections c 
        WHERE c.user_id = (SELECT id FROM users WHERE username = %s)
        ORDER BY c.name
    ''', (session['username'],))
    collections = cursor.fetchall()

    search_query = ''
    selected_collection = None
    message = None
    search_results = []

    if request.method == 'POST':
        collection_id = request.form.get('collection_id')
        search_query = request.form.get('search_query', '').strip()

        if collection_id and search_query:
            # Get the selected collection details
            cursor.execute('SELECT * FROM collections WHERE id = %s', (collection_id,))
            selected_collection = cursor.fetchone()

            # Try to find by ISBN (exact match, numeric or string)
            cursor.execute('SELECT * FROM books WHERE isbn = %s', (search_query,))
            book = cursor.fetchone()

            # If not found by ISBN, try by title (case-insensitive)
            if not book:
                cursor.execute('SELECT * FROM books WHERE LOWER(title) = %s', (search_query.lower(),))
                book = cursor.fetchone()

            if book:
                # Check if book already exists in collection
                cursor.execute('SELECT * FROM collection_books WHERE collection_id = %s AND book_id = %s',
                               (collection_id, book['id']))
                if not cursor.fetchone():
                    cursor.execute('INSERT INTO collection_books (collection_id, book_id) VALUES (%s, %s)',
                                   (collection_id, book['id']))
                    conn.commit()
                    message = f"Book '{book['title']}' added to collection!"
                else:
                    message = f"Book '{book['title']}' is already in this collection."
                search_results = [book]
            else:
                message = "No book found with that ISBN or title."

    cursor.close()
    conn.close()

    return render_template(
        'Items_click.html',
        collections=collections,
        selected_collection=selected_collection,
        search_query=search_query,
        search_results=search_results,
        message=message
    )

@app.route('/add_items_search')
def add_items_search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('add search.html')

@app.route('/personal_collection/<int:collection_id>')
def personal_collection(collection_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Get search parameters
    search_query = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'az')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get the specific collection
    cursor.execute('''
        SELECT c.*, COUNT(cb.book_id) as book_count 
        FROM collections c 
        LEFT JOIN collection_books cb ON c.id = cb.collection_id 
        WHERE c.id = %s AND c.user_id = (SELECT id FROM users WHERE username = %s)
        GROUP BY c.id
    ''', (collection_id, session['username']))
    collection = cursor.fetchone()
    
    if not collection:
        flash('Collection not found or not authorized!')
        return redirect(url_for('library'))
    
    # Build the base query for books
    query = '''
        SELECT b.* 
        FROM books b 
        JOIN collection_books cb ON b.id = cb.book_id 
        WHERE cb.collection_id = %s
    '''
    params = [collection_id]

    # Add search filter if search query exists
    if search_query:
        query += '''
            AND (
                LOWER(b.title) LIKE %s 
                OR LOWER(b.author) LIKE %s 
                OR LOWER(b.genre) LIKE %s
                OR b.isbn LIKE %s
            )
        '''
        search_pattern = f'%{search_query.lower()}%'
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

    # Add sorting
    if sort == 'za':
        query += ' ORDER BY b.title DESC'
    else:
        query += ' ORDER BY b.title ASC'

    # Execute the query
    cursor.execute(query, params)
    books = cursor.fetchall()
    
    # Get all collections for the user (for navigation)
    cursor.execute('''
        SELECT c.*, COUNT(cb.book_id) as book_count 
        FROM collections c 
        LEFT JOIN collection_books cb ON c.id = cb.collection_id 
        WHERE c.user_id = (SELECT id FROM users WHERE username = %s)
        GROUP BY c.id
    ''', (session['username'],))
    collections = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('personal_collection.html', 
                         collection=collection,
                         books=books,
                         collections=collections,
                         search_query=search_query,
                         sort=sort)

@app.route('/collection_view')
def collection_view():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('library'))  # Redirect to library for consistent layout

@app.route('/support')
def support():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('support.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/delete_collection/<int:collection_id>', methods=['POST'])
def delete_collection(collection_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    # Ensure the collection belongs to the current user
    cursor.execute('SELECT id FROM users WHERE username = %s', (session['username'],))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        flash('User not found!')
        return redirect(url_for('library'))
    user_id = user[0] if isinstance(user, tuple) else user['id']
    cursor.execute('SELECT id FROM collections WHERE id = %s AND user_id = %s', (collection_id, user_id))
    collection = cursor.fetchone()
    if not collection:
        cursor.close()
        conn.close()
        flash('Collection not found or not authorized!')
        return redirect(url_for('library'))
    # Delete books from collection_books first (to maintain referential integrity)
    cursor.execute('DELETE FROM collection_books WHERE collection_id = %s', (collection_id,))
    # Delete the collection itself
    cursor.execute('DELETE FROM collections WHERE id = %s', (collection_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Collection deleted successfully!')
    return redirect(url_for('library'))

@app.route('/delete_books_from_collection/<int:collection_id>', methods=['POST'])
def delete_books_from_collection(collection_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    book_ids = request.form.getlist('book_ids')
    if book_ids:
        conn = get_db_connection()
        cursor = conn.cursor()
        format_strings = ','.join(['%s'] * len(book_ids))
        cursor.execute(f"DELETE FROM collection_books WHERE collection_id = %s AND book_id IN ({format_strings})", [collection_id] + book_ids)
        conn.commit()
        cursor.close()
        conn.close()
        flash(f"Deleted {len(book_ids)} book(s) from the collection.")
    else:
        flash("No books selected for deletion.")
    return redirect(url_for('personal_collection', collection_id=collection_id))

if __name__ == '__main__':
    app.run(debug=True)
