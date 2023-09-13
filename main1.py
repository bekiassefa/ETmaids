import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'photo' not in request.files:
		flash('No file part')
		return redirect(request.url)
	photo = request.files['photo']
	if photo.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if photo and allowed_file(photo.filename):
		filename = secure_filename(photo.filename)
		photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		#return ('', 204)
		return render_template('upload.html', filename=filename)
		#return render_template('upload.html')
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename))
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)