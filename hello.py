from flask import Flask, request, jsonify, abort, url_for, redirect, render_template, send_file
from joblib import dump, load
import numpy as np
import pandas as pd
from datetime import datetime
knn = load('knn.joblib') 

app = Flask(__name__)

@app.route("/")
def hello():
    print('Hi!!!0!')
    return "<h1>Hello, my best friend, Masha!</h1>"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {username}'

def means(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums_avg = mean(nums)
    return str(nums_avg)

@app.route('/iris/<params>')
def iris(params):

    params = params.split(',')
    params = [float(param) for param in params]
    
    params = np.array(params).reshape(1,-1)
    return str(knn.predict(params))

@app.route('/show_image')
def show_image():

    return '<img src="static/setosa.jpg" alt="setosa">'

@app.route('/badrequest400')
def bad_request():
    abort(400)

@app.route('/iris_post', methods=['POST'])
def add_message():
    try:
        content = request.get_json()
        print(content)

        params = content['flower'].split(',')
        params = [float(param) for param in params]
        
        params = np.array(params).reshape(1,-1)
        predict = knn.predict(params)
        predict = {'class': str(predict[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(predict)

from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    print(form.name)
    if form.validate_on_submit():
        f = form.file.data
        df = pd.read_csv(f, header = None)
        print(df.head())

        #filename = secure_filename(f.filename)
        filename = form.name.data + '.csv'
        # f.save(os.path.join(
        #     filename
        # ))
        
        predict = knn.predict(df)
        print(predict)
        result = pd.DataFrame(predict)
        result.to_csv(filename, index = False)


        print(form.name)
        return send_file(filename,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)
    return render_template('submit.html', form=form)

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''