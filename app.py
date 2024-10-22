# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# In-memory bookmarks database
bookmarks = []
bookmark_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', bookmarks=bookmarks)

@app.route('/bookmark', methods=['POST'])
def create_bookmark():
    global bookmark_id_counter
    data = request.json
    bookmark = {
        'id': bookmark_id_counter,
        'title': data['title'],
        'url': data['url'],
        'category': data.get('category', ''),
        'favorite': False
    }
    bookmarks.append(bookmark)
    bookmark_id_counter += 1
    return jsonify(bookmark), 201

@app.route('/bookmark/<int:bookmark_id>', methods=['GET'])
def get_bookmark(bookmark_id):
    for bookmark in bookmarks:
        if bookmark['id'] == bookmark_id:
            return jsonify(bookmark), 200
    return jsonify({'error': 'Bookmark not found'}), 404

@app.route('/bookmark/<int:bookmark_id>', methods=['PUT'])
def update_bookmark(bookmark_id):
    data = request.json
    for bookmark in bookmarks:
        if bookmark['id'] == bookmark_id:
            bookmark.update(data)
            return jsonify(bookmark), 200
    return jsonify({'error': 'Bookmark not found'}), 404

@app.route('/bookmark/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    global bookmarks
    bookmarks = [b for b in bookmarks if b['id'] != bookmark_id]
    return jsonify({'message': 'Bookmark deleted'}), 200

@app.route('/bookmark/<int:bookmark_id>/favorite', methods=['PUT'])
def favorite_bookmark(bookmark_id):
    for bookmark in bookmarks:
        if bookmark['id'] == bookmark_id:
            bookmark['favorite'] = not bookmark['favorite']
            return jsonify(bookmark), 200
    return jsonify({'error': 'Bookmark not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
