import os
import sqlite3
from flask import (Flask, request, g, redirect, url_for, \
     abort, render_template, flash)
from contextlib import closing
from werkzeug.utils import secure_filename
from flask import send_from_directory

# Config
DATABASE = '/tmp/upld.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

UPLOAD_FOLDER = '/tmp/upload'
ALLOWED_EXTENSIONS = set(['jpg','png', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#Standard solve upload file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            g.db.execute('insert into entries (photoPath, comm, author) values (?, ?,?)',
                   [filename, request.form['comm'],request.form['author']])
            g.db.commit()
            uploaded_file(filename)
            return redirect(url_for('home'))
    return render_template('upload_photo.html')


@app.route('/<filename>')
def uploaded_file(filename):
     return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)

@app.route('/')
def home():
    cur = g.db.execute('select photoPath, comm, author from entries order by id desc')
    entries = [dict(photoPath=row[0], comm=row[1], author=row[2]) for row in cur.fetchall()]
    return render_template('home.html',entries=entries)

if __name__ == '__main__':
    app.debug = True
    app.run()