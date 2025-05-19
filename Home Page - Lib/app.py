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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user[0], password):
            session['logged_in'] = True
            session['username'] = username
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
    return render_template('Home Page - Lib.html')

@app.route('/library')
def library():
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
            ORDER BY b.title  -- Add ordering to maintain consistent display
        ''', (session['username'],))
        books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('Home Page - Lib.html', 
                         collections=collections,
                         books=books)

@app.route('/add_items')
def add_items():
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
    
    cursor.close()
    conn.close()
    
    return render_template('add_items.html', collections=collections)

@app.route('/add_collection', methods=['GET', 'POST'])
def add_collection():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        language = request.form.get('language', 'en')  # Get language from form
        
        if not collection_name:
            flash('Collection name is required!')
            return render_template('add_collection.html')
            
        # Get user_id from username in session
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if not user:
            flash('User not found!')
            cursor.close()
            conn.close()
            return render_template('add_collection.html')
            
        user_id = user[0]
        cursor.execute('INSERT INTO collections (name, user_id, language) VALUES (%s, %s, %s)', 
                      (collection_name, user_id, language))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Collection added successfully!')
        return redirect(url_for('library'))
    return render_template('add_collection.html')

@app.route('/add_items_click')
def add_items_click():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('Items_click.html')

@app.route('/add_items_search')
def add_items_search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('add search.html')

@app.route('/personal_collection')
def personal_collection():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('library'))  # Redirect to library for consistent layout

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

if __name__ == '__main__':
    app.run(debug=True)
