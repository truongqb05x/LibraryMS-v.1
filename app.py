from flask import Flask, render_template, request, jsonify, abort, url_for
from markupsafe import escape

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "Python Cơ Bản", "author": "Nguyễn Văn A", "year": 2020, "category": "Lập trình", "available": True},
    {"id": 2, "title": "Flask Nâng Cao", "author": "Trần Thị B", "year": 2021, "category": "Lập trình", "available": False},
    {"id": 3, "title": "Thiết Kế Web", "author": "Lê Văn C", "year": 2019, "category": "Đồ họa", "available": True},
    {"id": 4, "title": "Dữ Liệu Lớn", "author": "Phạm Thị D", "year": 2023, "category": "Khoa học", "available": True},
]

@app.route('/')
def index():
    total_books = len(BOOKS)
    available_books = sum(1 for b in BOOKS if b['available'])
    return render_template('index.html', total_books=total_books, available_books=available_books)

@app.route('/books')
def books_list():
    category = request.args.get('category')
    filtered_books = BOOKS
    if category:
        filtered_books = [b for b in BOOKS if b['category'] == category]
    
    # Get unique categories for the filter links
    categories = set(b['category'] for b in BOOKS)
    return render_template('books.html', books=filtered_books, categories=categories, current_category=category)

@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = next((b for b in BOOKS if b['id'] == book_id), None)
    if book is None:
        abort(404, description=f"Không có sách với ID = {escape(book_id)}")
    return render_template('book_detail.html', book=book)

@app.route('/api/books')
def api_books():
    return jsonify(BOOKS)

@app.route('/api/books/<int:book_id>')
def api_book_detail(book_id):
    book = next((b for b in BOOKS if b['id'] == book_id), None)
    if book is None:
        return jsonify({"error": f"Không có sách với ID = {escape(book_id)}"}), 404
    return jsonify(book)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error_msg=e.description), 404

if __name__ == '__main__':
    app.run(debug=True)
