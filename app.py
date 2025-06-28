

import flask
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

mock_book_database = {
    "978-3-16-148410-0": {"title": "The Art of Concurrent Programming", "status": "Available", "location": "Rak A-3"},
    "978-0-26-110221-7": {"title": "The Lord of The Rings", "status": "On Loan", "due_date": "2024-12-25"},
    "978-1-40-885565-2": {"title": "Harry Potter and the Philosopher's Stone", "status": "Available", "location": "Rak F-1"},
    "978-0-74-327356-5": {"title": "The Da Vinci Code", "status": "On Loan", "due_date": "2024-12-15"},
    "978-0-32-176572-3": {"title": "The C++ Programming Language", "status": "Available", "location": "Rak C-5"},
}
valid_isbns = list(mock_book_database.keys())

@app.route('/check_book_status', methods=['GET'])
def check_book_status():
    isbn_param = request.args.get('isbn')
    delay = random.uniform(0.1, 0.4)
    time.sleep(delay)
    if isbn_param:
        if isbn_param in mock_book_database:
            data = mock_book_database[isbn_param]
            data["isbn"] = isbn_param
            print(f"[SERVER] Sending status for ISBN {isbn_param}: {data} (after {delay:.2f}s delay)")
            return jsonify(data)
        else:
            error_msg = {"error": "isbn_not_found", "message": f"Book with ISBN '{isbn_param}' not found in the catalog."}
            print(f"[SERVER] ISBN {isbn_param} not found (after {delay:.2f}s delay)")
            return jsonify(error_msg), 404
    else:
        error_msg = {"error": "bad_request", "message": "ISBN parameter is required."}
        return jsonify(error_msg), 400

if __name__ == '__main__':
    print("Simple Library API Server running on http://127.0.0.1:5000")
    print("Endpoint: GET /check_book_status?isbn=978-3-16-148410-0")
    app.run(debug=False, threaded=True, use_reloader=False)
