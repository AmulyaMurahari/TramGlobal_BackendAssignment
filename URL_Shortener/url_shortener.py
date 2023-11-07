from flask import Flask, jsonify, request, redirect
import sqlite3
import string
import random
import re

app = Flask(__name__)

DATABASE = 'url_shortener.db'


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY, long_url TEXT NOT NULL, short_url TEXT UNIQUE NOT NULL, user_id TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id TEXT PRIMARY KEY, tier INTEGER NOT NULL)''')


init_db()


def get_short_url(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def validate_url(url):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return re.match(pattern, url) is not None


@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json

    # Check if required parameters are present
    if not data or 'long_url' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400

    long_url = data['long_url']
    user_id = data['user_id']

    # Validate URL
    if not validate_url(long_url):
        return jsonify({'error': 'Invalid URL provided'}), 400

    # Check if user exists and their tier
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tier FROM users WHERE user_id=?", (user_id,))
        user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 400

    # Define tier limits
    tier_limits = {
        1: 1000,  # Tier 1 limit
        2: 100    # Tier 2 limit
    }

    # Get the user's tier and limit
    tier = user[0]
    limit = tier_limits.get(tier, 0)  # Default to 0 if tier not found

    # Check user's current usage against their tier limit
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM urls WHERE user_id=?", (user_id,))
        count = cursor.fetchone()[0]

        if count >= limit:
            return jsonify({'error': f'Request limit of {limit} reached for your tier'}), 400

    short_url = get_short_url()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO urls (long_url, short_url, user_id) VALUES (?, ?, ?)",
                           (long_url, short_url, user_id))
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Short URL already exists'}), 400

    return jsonify({'short_url': short_url})


@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT long_url, short_url FROM urls WHERE user_id=?", (user_id,))
        urls = cursor.fetchall()

    return jsonify(urls)


@app.route('/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT long_url FROM urls WHERE short_url=?", (short_url,))
        url = cursor.fetchone()

        if url:
            return redirect(url[0])
        else:
            return jsonify({'error': 'URL not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)

