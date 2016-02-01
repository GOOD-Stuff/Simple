import os
import sqlite3
from flask import (Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash)
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed
from contextlib import closing

#TODO: Add Flask-Upload?
#TODO: Add Flask-Login?
#TODO: Add Flask-Cache?

# Config
DATABASE = '/tmp/simple.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = set(['jpg','png', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

### Enable database ###
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
#######################

#class Photo:


# Uploads
#uploaded_photos = UploadSet('photos', IMAGES)
#configure_uploads(app,uploaded_photos)

# Flask-Upload style
#@app.route('/upload', methods=['GET', 'POST'])
#def upload():
#    if request.method == 'POST' and 'photo' in request.files:
#        filename = uploaded_photos.save(request.files['photo'])
#        rec = Photo(filename=filename, user=g.user.id)
#        rec.store()
#        flash("Photo saved.")
#        return redirect(url_for('show', id=rec.id))
#    return render_template('upload.html')

#@app.route('/photo/<id>')
#def show(id):
#    photo = Photo.load(id)
#    if photo is None:
#        abort(404)
#    url = photos.url(photo.filename)
#    return render_template('show.html', url=url, photo=photo)
################################################

#Standard solve upload file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return render_template('upload_photo.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



if __name__ == '__main__':
    app.run()