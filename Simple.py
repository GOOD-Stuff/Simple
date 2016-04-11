import os
import sqlite3
from flask import (Flask, request, g, redirect, url_for, \
     abort, render_template, jsonify)
from contextlib import closing
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask.ext.responses import json_response

# Config
DATABASE = '/tmp/upld.db' # Database place
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

UPLOAD_FOLDER = '/tmp/upload' # Uploaded files place
ALLOWED_EXTENSIONS = set(['jpg','png', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # The restriction on file size - 16 MB
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

### Standard solve upload file ###
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Upload on server
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            g.db.execute('insert into entries (photoPath, comm) values (?, ?)',
                   [filename, request.form['comm']])
            g.db.commit()
            uploaded_file(filename)
            return redirect(url_for('home'))
    return render_template('upload_photo.html')

# Upload photo from client side
@app.route('/<filename>')
def uploaded_file(filename):
     return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)
######################################
@app.route('/json')
def getjson():
    cur = g.db.execute('select photoPath, comm from entries order by id desc')
    #entries = {row[0]: row[1] for row in cur.fetchall()}
    entries = [dict(photoPath=row[0], comm=row[1]) for row in cur.fetchall()]
    print(type(entries))
    print(entries)
    #resp = Response(response=data, status=200, mimetype="application/json")
    #return(resp)
    #see on http://texnolog.org/flask/ajax
    return jsonify(result=entries)#success=True, result=entries)#json_response(entries, status_code=201)

# Start page, show all from db
@app.route('/')
def home():
    cur = g.db.execute('select photoPath, comm from entries order by id desc')
    entries = [dict(photoPath=row[0], comm=row[1]) for row in cur.fetchall()]
    getjson()
    return render_template('home.html',entries=entries)

if __name__ == '__main__':
    app.debug = True
    app.run()