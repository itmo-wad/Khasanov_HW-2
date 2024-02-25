from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


client = MongoClient('mongodb://localhost:27017/')
db = client['auth_demo']
users_collection = db['users']


def is_logged_in():
    return 'username' in session


@app.route('/', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('profile'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect(url_for('login'))
    username = session['username']
    return render_template('profile.html', username=username)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
