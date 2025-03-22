from flask import Flask, request, jsonify
import sqlite3
from flask import render_template

app = Flask(__name__)


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS books(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   category TEXT NOT NULL,
                   author TEXT NOT NULL,
                   image_url TEXT NOT NULL
                   )""")
        print("Database initialized.")


init_db()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def list_books():
    with sqlite3.connect("database.db") as conn:
        books = conn.execute("SELECT * FROM books").fetchall()

    stored_books = []

    for book in books:
        books_dict = {
            "id": book[0],
            "title": book[1],
            "category": book[2],
            "author": book[3],
            "image_url": book[4]
        }
        stored_books.append(books_dict)

    return jsonify(stored_books)

@app.route('/donate', methods=['POST'])
def add_book():
    new_book = request.get_json()

    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO books (title, category, author, image_url) VALUES (?, ?, ?, ?)",
                     (new_book['title'], new_book['category'], new_book['author'], new_book['image_url']))

    return jsonify({"message": "Book added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
