from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Taskin'}
    posts = [
        {
            'author': {'username': 'Safwan'},
            'body': 'Had a great time at the BBQ!'
        },
        {
            'author': {'username': 'Hisham'},
            'body': 'Beautiful day in Jeddah!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)