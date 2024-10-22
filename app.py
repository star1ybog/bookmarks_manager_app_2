from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from utils import validate_email, create_jwt_token, decode_jwt_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin'

users = {}

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
    
    # Перевірка на дублювання (за URL або за заголовком)
    for bookmark in bookmarks:
        if bookmark['url'] == data['url']:
            return jsonify({'message': 'Bookmark already exists!'}), 400
    
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


# Декоратор для захисту маршрутів
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            return redirect(url_for('login'))
        try:
            data = decode_jwt_token(token)
        except:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        email = data['email']
        password = data['password']
        password_check = data['password_check']
        
        # Валідація
        if not all([username, email, password, password_check]):
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect(url_for('register'))
        
        if password != password_check:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        
        if not validate_email(email):
            flash('Invalid email address.', 'error')
            return redirect(url_for('register'))

        # Хешування пароля
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Зберігання користувача
        users[username] = {
            'email': email,
            'password': hashed_password,
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name')
        }

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        user = users.get(username)

        if not user or not check_password_hash(user['password'], password):
            flash('Invalid credentials.', 'error')
            return redirect(url_for('login'))

        # Створення JWT токена
        token = create_jwt_token(username)

        resp = make_response(redirect(url_for('content')))
        resp.set_cookie('access_token', token, httponly=True)
        return resp

    return render_template('login.html')

@app.route('/logout')
@token_required
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('access_token')
    return resp

@app.route('/content')
@token_required
def content():
    token = request.cookies.get('access_token')
    data = decode_jwt_token(token)
    username = data['username']
    
    # Групуємо закладки за категоріями
    categorized_bookmarks = {}
    for bookmark in bookmarks:
        category = bookmark.get('category', 'Uncategorized')
        if category not in categorized_bookmarks:
            categorized_bookmarks[category] = []
        categorized_bookmarks[category].append(bookmark)

    # Сортуємо закладки за заголовком в кожній категорії
    for category in categorized_bookmarks:
        categorized_bookmarks[category].sort(key=lambda b: b['title'])

    return render_template('index.html', username=username, categorized_bookmarks=categorized_bookmarks)



if __name__ == '__main__':
    app.run(debug=True)