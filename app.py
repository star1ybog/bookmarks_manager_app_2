from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# In-memory bookmarks database
bookmarks = []
bookmark_id_counter = 1

@app.route('/')
def index():
    # Group bookmarks by category and sort them by title
    categorized_bookmarks = {}
    for bookmark in bookmarks:
        category = bookmark.get('category', 'Uncategorized')
        if category not in categorized_bookmarks:
            categorized_bookmarks[category] = []
        categorized_bookmarks[category].append(bookmark)

    # Sort bookmarks by title within each category
    for category in categorized_bookmarks:
        categorized_bookmarks[category].sort(key=lambda b: b['title'])

    return render_template('index.html', categorized_bookmarks=categorized_bookmarks)

@app.route('/bookmark/<int:bookmark_id>', methods=['GET'])
def get_bookmark(bookmark_id):
    # View individual bookmark by ID
    for bookmark in bookmarks:
        if bookmark['id'] == bookmark_id:
            return render_template('bookmark_detail.html', bookmark=bookmark)
    return render_template('404.html'), 404

@app.route('/bookmark', methods=['POST'])
def create_bookmark():
    global bookmark_id_counter
    data = request.json
    bookmark = {
        'id': bookmark_id_counter,
        'title': data['title'],
        'url': data['url'],
        'category': data.get('category', 'Uncategorized'),
        'favorite': False
    }
    bookmarks.append(bookmark)
    bookmark_id_counter += 1
    return jsonify(bookmark), 201

@app.route('/bookmark/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    global bookmarks
    bookmarks = [b for b in bookmarks if b['id'] != bookmark_id]
    return jsonify({'message': 'Bookmark deleted'}), 200

@app.route('/bookmark/<int:bookmark_id>', methods=['PUT'])
def edit_bookmark(bookmark_id):
    data = request.json
    for bookmark in bookmarks:
        if bookmark['id'] == bookmark_id:
            bookmark['title'] = data['title']
            bookmark['url'] = data['url']
            bookmark['category'] = data.get('category', bookmark['category'])
            return jsonify(bookmark), 200
    return jsonify({'message': 'Bookmark not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)