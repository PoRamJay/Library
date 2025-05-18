from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return render_template('Home Page - Lib.html')

@app.route('/library')
def library():
    return render_template('Home Page - Lib.html')

@app.route('/add_items')
def add_items():
    return render_template('add_items.html')

@app.route('/add_collection')
def add_collection():
    return render_template('add_collection.html')

@app.route('/add_items_click')
def add_items_click():
    return render_template('Items_click.html')

@app.route('/add_items_search')
def add_items_search():
    return render_template('add search.html')

@app.route('/personal_collection')
def personal_collection():
    return render_template('personal_collection.html')

@app.route('/collection_view')
def collection_view():
    return render_template('collectionview.html')

if __name__ == '__main__':
    app.run(debug=True)
