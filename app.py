from flask import Flask, render_template, json, jsonify, request, redirect, url_for

import keras
from keras.preprocessing import image
from keras import backend as K

import datetime
import os
import base64
import tempfile
from time import time

app = Flask(__name__)

userID = 'none'
password = 'none'
model = None
graph = None

# Loading a keras model with flask
# https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
def load_model(Choice):
    global model
    global graph
    print(Choice)
    if (Choice == "Alpha"):
        K.clear_session()
        model = keras.models.load_model("emnist/eminst_letters_dense_model.h5")
    elif (Choice == "Num"):  
        K.clear_session() 
        model = keras.models.load_model("emnist/eminst_digits_dense_model.h5")   
    graph = K.get_session().graph

def ascii_map():
    mapping_file = 'emnist/emnist-letters-mapping.txt'
    with open(mapping_file, 'r') as fin:
        mapping = fin.readlines()
    ascii_map = {}
    for line in mapping:
        char_class = int(line.split()[0])
        letter = chr(int(line.split()[1]))
        ascii_map[char_class] = letter
    return(ascii_map)

def prepare_image(img):
    from keras.preprocessing.image import img_to_array
    image = img_to_array(img)
    # Scale the image pixels by 255 (or use a scaler from sklearn here)
    image= 255 - (image)
    # Flatten into a 1x28*28 array
    image = image.flatten().reshape(-1, 28*28)
    return(image)

@app.route("/")
def main():
    return render_template('login.html')

@app.route('/home',  methods=['GET', 'POST'])
def home():
    return render_template('index.html')    

@app.route('/about',  methods=['GET', 'POST'])
def about():
    return render_template('ShellLearn_About.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            userID = request.form['username']
            password = request.form['password']
            return redirect(url_for('about'))
    return render_template('login.html', error=error)
 
@app.route('/ShellLearn_book', methods=['GET', 'POST'])
def level1ABC():
    # if userID != 'none' :
        return render_template('ShellLearn_book.html')
    # else:
    #    return render_template('login.html') 

@app.route('/letters', methods=['GET', 'POST'])
def get_letters_html():

    return render_template('letters.html')

@app.route('/numbers', methods=['GET', 'POST'])
def get_numbers_html():

    return render_template('numbers.html')

TMP_DIR_NAME = 'Images'

Choice = " "

@app.route("/Alphabets/", methods=['POST'], endpoint="Alphabets")
def Alphabets():
    Choice = "Alpha"
    load_model(Choice)
    Choice = " "
    filename = '{:10d}.png'.format(int(time()))  # generate some filename
    filepath = os.path.join(TMP_DIR_NAME, filename)

    with open(filepath, "wb") as fh:
         base64_data = request.json['image'].replace('data:image/png;base64,', '')
         fh.write(base64.b64decode(base64_data))
    
    # data = {"success": False}
    data = {}
    # Load the saved image using Keras and resize it to the mnist # format of 28x28 pixels
    image_size = (28, 28)
    im = image.load_img(filepath, target_size=image_size, grayscale=True)

    # Convert the 2D image to an array of pixel values
    image_array = prepare_image(im)
   
    # Get the tensorflow default graph and use it to make predictions
    global graph
    with graph.as_default():
        amap = ascii_map()
        # Use the model to make a prediction
        predicted_digit = model.predict_classes(image_array)[0]
        pred_letter = amap[predicted_digit+1]
        data["prediction"] = pred_letter
        # indicate that the request was a success
        # data["success"] = True

    return jsonify(data)   

@app.route("/Numbers/", methods=['POST'], endpoint="Numbers")
def Numbers():
    Choice = "Num"
    load_model(Choice)
    Choice = " "
    filename = '{:10d}.png'.format(int(time()))  # generate some filename
    filepath = os.path.join(TMP_DIR_NAME, filename)

    with open(filepath, "wb") as fh:
         base64_data = request.json['image'].replace('data:image/png;base64,', '')
         fh.write(base64.b64decode(base64_data))

    # data = {"success": False}
    data = {}
    # Load the saved image using Keras and resize it to the mnist # format of 28x28 pixels
    image_size = (28, 28)
    im = image.load_img(filepath, target_size=image_size, grayscale=True)

    # Convert the 2D image to an array of pixel values
    image_array = prepare_image(im)
    # print(image_array)

    # Get the tensorflow default graph and use it to make predictions
    global graph
    with graph.as_default():
        amap = ascii_map()
        # Use the model to make a prediction
        predicted_digit = model.predict_classes(image_array)[0]
        # pred_letter = amap[predicted_digit+1]
        data["prediction"] = int(predicted_digit)
        # indicate that the request was a success
        # data["success"] = True

    return jsonify(data)       


if __name__ == "__main__":
    app.run(debug=True)