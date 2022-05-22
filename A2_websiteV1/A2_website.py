# -*- coding: utf-8 -*-
"""
Created on Wed May 18 08:54:54 2022

@author: Mikhail Vainarevich
"""

import os

#Website libraries
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import numpy as np
import PIL
from tensorflow.keras.preprocessing import image
from keras.models import load_model
#from keras.backend import set_session
#import tensorflow as tf

# Categories
categories = np.array(['battery','biological','cardboard','clothes','glass','metal','paper','plastic','shoes','trash'])

X = 'Waste'
Y = 'Recyclable'

#Example photos

sample_BA = 'static/battery.jpg'
sample_BI = 'static/biological.jpg'
sample_CA = 'static/cardboard.jpg'
sample_CL = 'static/clothes.jpg'
sample_GL = 'static/glass.jpg'
sample_ME = 'static/metal.jpg'
sample_PA = 'static/paper.jpg'
sample_PL = 'static/plastic.jpg'
sample_SH = 'static/shoes.jpg'
sample_TR = 'static/trash.jpg'
sampleX = 'static/Waste.jpg'
sampleY = 'static/Recyclable.jpg'

#User uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}




app = Flask(__name__)

def load_model_from_file():
    myModel = load_model('garbage_class_model.h5')
    return(myModel)

#Allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#Define the view for the top level page
@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method =='GET':
        return render_template('index.html',myX=X,myY=Y,mySampleX=sampleX,mySampleY=sampleY)
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename =='':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('I only accept files of type'+str(ALLOWED_EXTENSIONS))
            return redirect(request.url)
        #When file is correct
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('uploaded_file', filename=filename))
        
@app.route('/uploads/<filename>')       
def uploaded_file(filename):
    test_image = image.load_img(UPLOAD_FOLDER+"/"+filename,target_size = (128,128))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    
    #mySession = app.config['SESSION']
    myModel = app.config['MODEL']
    #myGraph = app.config['GRAPH']
    #with myGraph.as_default():
        #set_session(mySession)
    result = myModel.predict(test_image).argmax(axis=-1)
    result_cat = categories[result]
    image_src = "/"+UPLOAD_FOLDER +"/"+filename
    recyclable = np.array(['cardboard','glass','metal','paper','plastic'])
    waste = np.array(['biological','clothes', 'shoes','trash'])
    special = np.array(['battery'])
    if result_cat in recyclable:
        answer = "<div class='col text-center'><img_width='128' height='128' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+Y+" "+str(result_cat)+"</h4></div><div class='col'></div><div class='w-100'></"
    elif result_cat in waste:
        answer = "<div class='col'></div><div class='col text-center'><img width='128' height='128' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+X+" "+str(result_cat)+"</h4></div><div class='w-100'></"            
    #battery
    elif result_cat in special:
        answer = "<div class='col'></div><div class='col text-center'><img width='128' height='128' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+"recycle in specialised place"+" "+str(result_cat)+"</h4></div><div class='w-100'></"            
    results.append(answer)
    return render_template('index.html',myX=X,myY=Y,mySampleX=sampleX,mySampleY=sampleY, len=len(results),results=results)


def main():
    myModel = load_model_from_file()
    
    app.config['SECRET_KEY'] = 'secret_key'
#    app.config['SESSION'] = mySession
    app.config['MODEL'] = myModel
#    app.config['GRAPH'] = myGraph
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
    app.run()
      
    


#Create running list of results
results = []

#launch everything

main()