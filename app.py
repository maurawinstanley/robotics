# app.py
import sqlite3
import service
#import request
from flask import send_file
from flask import request, render_template, jsonify, Flask , session, url_for , redirect

from flask_dropzone import Dropzone

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
dropzone = Dropzone(app)
#https://medium.com/bhavaniravi/build-your-1st-python-web-app-with-flask-b039d11f101c
#https://medium.com/@dustindavignon/upload-multiple-images-with-python-flask-and-flask-dropzone-d5b821829b1d


#app.config['SECRET_KEY'] = 'secretkeyyyyyy'

app.secret_key = "secretkeyme"

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB



UPLOAD_FOLDER = '/Documents/robo/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
urls = None 




@app.route('/upload_image', methods = ["POST"])
def upload_file():
    print("post ")
    if request.method == 'POST':
        print("in post ")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        print("not in post")



'''@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
    return json.dumps({'filename':f_name})'''

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    global file_url_global

    # handle image upload from Dropszone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )

            # append image urls
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        file_url_global = file_urls
        urls = file_urls
        return "uploading..."
    # return dropzone template on GET request    
    return render_template('index.html')


@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    
    file_urls = session['file_urls']
    file_url_global = file_urls
    session.pop('file_urls', None)
    
    return render_template('results.html', file_urls=file_urls)





@app.route('/images', methods=['GET'])
def images():
    print("urls: ", urls)
    print("in the image function")
    # redirect to home if no images to display
    #if "file_urls" not in session or session['file_urls'] == []:
        #return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    #file_urls = session['file_urls']
    print(file_url_global[0], " is file url ")
    session.pop('file_urls', None)
    #print(file_urls, " is the file url ")
    return file_url_global[0]
    return send_file(file_url_global[0], mimetype = 'image/png')
    #return send_file(file_url_global[0], mimetype='image/png', attachment_filename="img2.jpg", as_attachment=True)



@app.route("/<name>")              # at the end point /<name>
def hello_name(name):              # call method hello_name
    return "Hello "+ name  


@app.route("/color", methods =["POST"])
def create_color():
    return service.ColorsService().create(jsonify(request.json))


@app.route("/color", methods =["GET"])
def render_color():
    return service.ColorsService().get()




class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('colors.db')
        self.create_person_table()
        self.create_colors_table()
        # Why are we calling user table before to_do table
        # what happens if we swap them?

    def create_colors_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Colors" (
          
          Color TEXT
          
          
        );
        """
        #id INTEGER PRIMARY KEY,
        #UserId INTEGER FOREIGNKEY REFERENCES User(_id)

        self.conn.execute(query)
    def create_person_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Person" (
          id INTEGER PRIMARY KEY,
          Name TEXT,
          
          UserId INTEGER FOREIGNKEY REFERENCES Person(_id)
        );
        """

'''important: 
to get the image downloaded: 
import shutil

import requests
url = "http://localhost:5000/images"
new_url = requests.get(url)
new_url = new_url.content.decode('utf-8')
response = requests.get(new_url, stream=True)
with open('img2.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
    '''



if __name__ == "__main__":
	Schema()        # on running python app.py
	app.run(debug = True) 


