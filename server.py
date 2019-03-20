from flask import Flask, render_template, request, redirect, send_from_directory
import numpy as np
import cv2
from tool import Tool, loading
from datetime import datetime
import os
import string
import random

ORG_DIR = "./images/origins"
SAVE_DIR = "./images/treated"
TEMP_DIR = "./images/temp"

if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)
if not os.path.isdir(ORG_DIR):
    os.mkdir(ORG_DIR)

app = Flask(__name__, static_url_path="")


def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])


@app.route('/')
def index():
    return render_template('index.html', temp=os.listdir(TEMP_DIR))

@app.route('/archive')
def archive():
    return render_template('archive.html', images=os.listdir(SAVE_DIR)[::-1])

@app.route('/images/origins/<path:path>')
def send_origin(path):
    return send_from_directory(ORG_DIR, path)


@app.route('/images/treated/<path:path>')
def send_treated(path):
    return send_from_directory(SAVE_DIR, path)

@app.route('/images/temp/<path:path>')
def send_temp(path):
    return send_from_directory(TEMP_DIR, path)

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b


@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        org = cv2.imdecode(img_array, 1)
        print(org.shape)
        org = cv2.resize(org, (org.shape[1]//2, org.shape[0]//2))
        func = Tool()
        param = [org]

        # 変換
        if request.form['ways'] == '0':
            loading(func.keeping, param)
            img = func.result[0]
            print('')
            print('done')

        elif request.form['ways'] == '1':
            loading(func.pencil_drawing, param)
            img = func.result[0]
            print('')
            print('done')

        elif request.form['ways'] == '2':
            loading(func.ink_painting, param)
            img = func.result[0]
            print('')
            print('done')

        elif request.form['ways'] == '3':
            loading(func.animated, param)
            img = func.result[0]
            print('')
            print('done')

        elif request.form['ways'] == '4':
            loading(func.manga_filter, param)
            img = func.result[0]
            print('')
            # print('done')
        # clear result
        # func.clear()

        org = cv2.resize(org, (org.shape[1]*2, org.shape[0]*2))
        img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))
        # 画像保存
        dt_now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_") + random_str(5)

        org_path = os.path.join(ORG_DIR, dt_now + ".jpg")
        save_path = os.path.join(SAVE_DIR, dt_now + ".jpg")
        cv2.imwrite(org_path, org)
        cv2.imwrite(save_path, img)

        for i in os.listdir(TEMP_DIR):
            os.remove(TEMP_DIR + '/' + i)

        t = random_str(5)
        cv2.imwrite(TEMP_DIR + "/org_temp_{}.jpg".format(t), org)
        cv2.imwrite(TEMP_DIR + "/treat_temp_{}.jpg".format(t), img)

        # temp保存
        print("save")

        return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
