from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import numpy as np 
import pandas as pd 
import cv2
from random import randint
from audio import encode
from audio import decode
from text import encode_data
from text import decode_data
from image import merge
from image import unmerge


app= Flask(__name__)

# s1=cv2.imread("s1.png")
# s2=cv2.imread("s.png")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/image')
def image():
    
    merge('3.png','5.png')
    return "who let the dogs out "
    
@app.route('/decode')
def imagedecode():
    unmerge('merged.png')
    return "u cant kill me"

@app.route('/audio')
def audio():
    encode()
    decode()
    return render_template('cool.html')
 
@app.route('/', methods=['POST','GET'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        last_name = request.form.get("fname") 
        print(last_name)
        file.save(file.filename)
        img = cv2.imread(file.filename)
        encode_data(img,last_name)
        image1=cv2.imread("s.png")
        decode_data(image1)
        return render_template('cool.html')

@app.route('/endecrypt', methods=['POST','GET'])
def filess_render():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        cryptopt = request.form.get("endebtn")
        return render_template('files.html',cryptopt=cryptopt,stegtype=stegotype)

@app.route('/encryptfiles', methods=['POST','GET'])
def text_aud_encrypt():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        print(stegotype)
        if stegotype=="Text" :
            file = request.files['opfile']
            secret_msg = request.form.get("hidefile") 
            print(secret_msg)
            file.save('opfile.png')
            img = cv2.imread("opfile.png")
            encode_data(img,secret_msg)
            # image1=cv2.imread("textstegofile.png")
            # decode_data(image1)
        
        if stegotype=="Audio":
            file = request.files['opfile']
            secret_msg = request.form.get("hidefile") 
            print(secret_msg)
            file.save('sample.WAV')
            print("saved")
            encode(secret_msg)
        return render_template('cool.html')

@app.route('/encryptimgfiles', methods=['POST','GET'])
def img_encrypt():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        print(stegotype)
        if stegotype=="Image" :
            file = request.files['opfile']
            file1 = request.files['hidefile']
            file.save('opfile.png')
            file1.save('hidefile.png')
            merge('opfile.png','hidefile.png')
        
        return render_template('cool.html',stegtype=stegotype)

@app.route('/decryptfiles', methods=['POST','GET'])
def text_aud_img_decrypt():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        print(stegotype)
        if stegotype=="Text" :
            file1 = request.files['opfile']
            file1.save('textstegofile1.png')
            image1=cv2.imread("textstegofile1.png")
            secretmsg=decode_data(image1)
        if stegotype=="Image" :
            file1 = request.files['opfile']
            file1.save('imgstegofile.png')
            unmerge('imgstegofile.png')
            secretmsg="img decryption done"
        if stegotype=="Audio" :
            file1 = request.files['opfile']
            file1.save('audstegofile.WAV')            
            secretmsg=decode()
        return render_template('cool.html',decodedata=secretmsg)

if __name__ == "__main__":
    app.run()
