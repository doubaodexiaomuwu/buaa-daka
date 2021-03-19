#!/usr/bin/python3  

# -*- coding: utf-8 -*-
# @Author   : Grayson
# @Time     : 2020-12-07 20:47
# @Email    : weipengweibeibei@163.com
# @Description  :

# encoding:utf-8
# !/usr/bin/env python
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import time
import os
import base64

from Pic_str import Pic_str
from buaa_daka_orc import get_daka

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'jpeg', 'PNG', 'gif', 'GIF'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_test():
    return render_template('up.html')


# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]
        new_filename = Pic_str().create_uuid() + '.' + ext
        join_path = os.path.join(file_dir, new_filename)
        print(join_path)
        f.save(join_path)
        notice_info = get_daka(join_path)

        return notice_info
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})

if __name__ == '__main__':
    app.run(debug=True)