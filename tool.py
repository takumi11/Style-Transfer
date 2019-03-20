# -*- coding: utf-8 -*-

import sys
import time
import cv2
import numpy as np
import threading


def loading(func, param):
    t = threading.Thread(target=func, args=(param))
    t.start()
    count = 1
    s_time = time.time()
    # スレッドが終わるまでループ
    while True:
        sys.stdout.write('\rNow Leading{}'.format('.'*count))
        sys.stdout.flush()
        time.sleep(1)
        count += 1
        if(not t.isAlive()):  # スレッドが終了していたらループを抜ける
            break
    print('')
    print('elapsed time: {}'.format(time.time()-s_time))


class Tool():
    def __init__(self):
        self.result = []

    def clear(self):
        self.result = []

    def keeping(self, org):
        output = org
        self.result.append(output)


    def pencil_drawing(self, org):

        kernel = np.ones((3,3),np.uint8)

        mono_img = cv2.cvtColor(org, cv2.COLOR_RGB2GRAY)
        dilate_img = cv2.dilate(mono_img, kernel, iterations=1)
        diff_img = cv2.absdiff(mono_img, dilate_img)
        diff_not_img = cv2.bitwise_not(diff_img)

        output = cv2.cvtColor(diff_not_img, cv2.COLOR_GRAY2RGB)

        self.result.append(output)


    def ink_painting(self, org):

        img_gray = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
        img_gray_inv = 255 - img_gray
        img_blur = cv2.GaussianBlur(img_gray_inv, ksize=(21, 21),sigmaX=0, sigmaY=0)
        output = cv2.divide(img_gray, 255-img_blur, scale=256)

        self.result.append(output)


    def animated(self, org):

        image = cv2.GaussianBlur(org, (5, 5), 0)
        output = cv2.pyrMeanShiftFiltering(image, 25, 25)

        self.result.append(output)


    def manga_filter(self, org):

        # グレースケール変換
        gray = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
        screen = cv2.imread("./materials/screen.jpg")
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        # スクリーントーン画像を入力画像と同じ大きさにリサイズ
        screen = cv2.resize(screen,(gray.shape[1],gray.shape[0]))

        th1 = 60
        th2 = 150
        # Cannyアルゴリズムで輪郭検出し、色反転
        edge = 255 - cv2.Canny(gray, th1, th2)

        # 三値化
        gray[gray <= th1] = 0
        gray[gray >= th2] = 255
        gray[ np.where((gray > th1) & (gray < th2)) ] = screen[ np.where((gray > th1)&(gray < th2)) ]

        # 三値画像と輪郭画像を合成
        output = cv2.bitwise_and(gray, edge)

        self.result.append(output)
