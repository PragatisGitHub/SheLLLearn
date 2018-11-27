from flask import Flask, jsonify, request, render_template, json, redirect, url_for

import keras
from keras.preprocessing import image
from keras import backend as K

import datetime
import os
import base64
import tempfile
from time import time

app = Flask(__name__)

userID = 'user1'
password = 'user1'
model = None
graph = None

import pymongo
try:
    myclient = pymongo.MongoClient("mongodb://admin:admin@shelllern-shard-00-00-xwhf2.gcp.mongodb.net:27017,shelllern-shard-00-01-xwhf2.gcp.mongodb.net:27017,shelllern-shard-00-02-xwhf2.gcp.mongodb.net:27017/ShellLern?ssl=true&replicaSet=ShellLern-shard-0&authSource=admin&retryWrites=true")
    mydb = myclient["ShellLern"]
    shell_coll = mydb["students"]
    # mydict = { "name": "John", "password": "Highway 37" }
    # x = shell_coll.insert_one(mydict)
    # print(x.inserted_id)
    #
    # print(myclient.list_database_names())
    # x = shell_coll.find_one()
    #
    # print(x)
    #
    # print(myclient.list_database_names())
except Exception as exc:
    print(exc)

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
        global userID
        userID= request.form['username'].lower()
        global password
        password= request.form['password'].lower()
        new_user = True
        for name in shell_coll.find({},{"name":1, "password":1}):
            if userID == name["name"] and password == name["password"]:
                new_user = False
                break
        if new_user:
            new_record = { "name": userID, "password": password, "letter": " ", "number": " " }
            x = shell_coll.insert_one(new_record)
        return redirect(url_for('about'))

 
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

Symbol = ''

@app.route("/Alphabets/", methods=['POST'], endpoint="Alphabets")
def Alphabets():
    Symbol = request.json['symbol']
#    print(Symbol)
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
        if pred_letter ==Symbol:
            data["result"] = True
        else:
            data["result"] = False
        # indicate that the request was a success
        # data["success"] = True
    for name in shell_coll.find({},{"name":1, "password":1}):
        if userID == name["name"] and password == name["password"]:
            new_record = { "name": userID, "password": password, "letter": data["result"], "number": " "}
            x = shell_coll.insert_one(new_record)
            break
        # counter for true anf false for current user
    trues=0
    falses=0
    for name in shell_coll.find({},{"name":1, "password":1, "letter":1}):
        if userID == name["name"] and password == name["password"]:
            if name["letter"] == True:
                trues+=1
            if name["letter"] == False:
                falses+=1
    data["trues"] = trues
    data["falses"] = falses


    return jsonify(data)   

@app.route("/Numbers/", methods=['POST'], endpoint="Numbers")
def Numbers():
    Symbol = request.json['symbol']
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
        if str(predicted_digit) ==Symbol:
            data["result"] = True
        else:
            data["result"] = False
        # indicate that the request was a success
        # data["success"] = True
    for name in shell_coll.find({},{"name":1, "password":1}):
        if userID == name["name"] and password == name["password"]:
            new_record = { "name": userID, "password": password, "number": data["result"], "letter": " " }
            x = shell_coll.insert_one(new_record)
            break
    # counter for true anf false for current user
    trues=0
    falses=0
    for name in shell_coll.find({},{"name":1, "password":1, "number":1}):
        if userID == name["name"] and password == name["password"]:
            if name["number"]== True:
                trues+=1
            if name["number"] == False:
                falses+=1
    data["trues"] = trues
    data["falses"] = falses


    return jsonify(data)       


if __name__ == "__main__":
    app.run(debug=True)