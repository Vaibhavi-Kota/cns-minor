from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import numpy as np
import pandas as pd
import cv2
from random import randint
from pydub import AudioSegment
from PIL import Image

import librosa


from flask import render_template, request, session, redirect, url_for


# from flask.ext.session import Session

from audio import encode
from audio import decode
from text import encode_data
from text import decode_data
from image import merge
from image import unmerge




# sess= Session()
app = Flask(__name__, static_folder='./static')
app.secret_key = "abc" 
# s1=cv2.imread("s1.png")
# s2=cv2.imread("s.png")


@app.route('/')
def home():
    return render_template('index1.html')


# @app.route('/audio', methods=['POST', 'GET'])
# def redi():
#     if request.method == 'GET':
#         return render_template('audio.html')

#     if request.method == 'POST':
#         file = request.files['opfile']
#         print(request.files['file'].filename)
#         secret_msg = request.form.get("hidefile")
#         print(secret_msg)
#         file.save('./static/audio/sample.wav')
#         print("saved")
#         encode(secret_msg)
#         return "yo"


@app.route('/endecrypt', methods=['POST', 'GET'])
def filess_render():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        cryptopt = request.form.get("endebtn")
        return render_template('files.html', cryptopt=cryptopt, stegtype=stegotype)


@app.route('/encryptfiles', methods=['POST', 'GET'])
def text_aud_encrypt():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        print(stegotype)
        if stegotype == "Text":
            file = request.files['opfile']
            secret_msg = request.form.get("hidefile")
            print(secret_msg)
            file.save('./static/text/opfile.png')
            img = cv2.imread("./static/text/opfile.png")
            encode_data(img, secret_msg)
            # image1=cv2.imread("textstegofile.png")
            # decode_data(image1)

        if stegotype == "Audio":
            file = request.files['opfile']
            print(file.filename)
            extension = file.filename.rsplit('.', 1)[1].lower()
            print(extension)
            if(extension == "mp3"):
                src = file
                dst = "test.wav"

                                                            
                sound = AudioSegment.from_mp3(src)
                sound.export('./static/audio/sample.wav', format="wav")
            else:
                file.save('./static/audio/sample.wav')


            

            secret_msg = request.form.get("hidefile")
            print(secret_msg)
            

            mins = librosa.get_duration(filename='./static/audio/sample.wav')
            print(mins)
            if(mins > 120):
                flash("Audio length should be reduced")
                return render_template('files.html',cryptopt="encrypt",stegtype=stegotype)
            
            print("saved")
            encode(secret_msg)
        return render_template('cool.html', stegtype=stegotype)


@app.route('/encryptimgfiles', methods=['POST', 'GET'])
def img_encrypt():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        print(stegotype)
        if stegotype == "Image":
            file = request.files['opfile']
            file1 = request.files['hidefile']
            file.save('./static/image/opfile.png')
            file1.save('./static/image/hidefile.png')

            img1 = Image.open('./static/image/opfile.png')
            img2 = Image.open('./static/image/hidefile.png')

            # Ensure image 1 is larger than image 2
            if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
                flash("Image 1 size is lower than image 2 size!")
                cryptopt = "encrypt"
                return render_template('files.html', cryptopt=cryptopt, stegtype=stegotype)

            else:
                merge('./static/image/opfile.png',
                      './static/image/hidefile.png')
                return render_template('cool.html', stegtype=stegotype)
    return render_template('cool.html', stegtype=stegotype)


@app.route('/decryptfiles', methods=['POST', 'GET'])
def text_aud_img_decrypt():
    if request.method == 'POST':
        stegotype = request.form.get("stegtype")
        decryptedtext = ""
        print(stegotype)
        if stegotype == "Text":
            file1 = request.files['opfile']
            file1.save('./static/text/textstegofile1.png')
            image1 = cv2.imread("./static/text/textstegofile1.png")
            secretmsg = "textdecryptiondone"
            decryptedtext = decode_data(image1)
        if stegotype == "Image":
            file1 = request.files['opfile']
            file1.save('./static/image/imgstegofile.png')
            unmerge('./static/image/imgstegofile.png')
            secretmsg = "imgdecryptiondone"
        if stegotype == "Audio":
            file1 = request.files['opfile']
            file1.save('./static/audio/audstegofile.wav')
            secretmsg = "Audiodecryptiondone"
            decryptedtext = decode()
        return render_template('cool.html', decodedata=secretmsg, decryptedtext=decryptedtext)

if __name__ == '__main__':  
    app.run(debug = True)  

