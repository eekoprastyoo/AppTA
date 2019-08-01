import cv2
import numpy as np
import os
import pygame


from gtts import gTTS
from io import BytesIO
from pathlib import Path
from natsort import natsorted
from tempfile import TemporaryFile

from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QLineEdit, QMessageBox, QVBoxLayout, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

fname = ""


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Advance Driver Asisten System'
        self.left = 0
        self.top = 0
        self.width = 1024
        self.height = 600
        self.setStyleSheet("QMainWindow {background-image: url(bg.png);}")
        self.initUI()

    # initUI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.btnOpen()
        self.btnProcess()
        self.btnExit()

        self.title_img_ori()
        self.label_img_ori()
        self.title_img_hasil()
        self.label_img_hasil()
        self.title_result()
        self.label_result()
        self.title_db()
        self.label_db()

        self.show()

    # button open

    def btnOpen(self):
        btn_open = QPushButton('OPEN', self)
        # button.setToolTip('This is an example button')
        btn_open.move(80, 40)
        btn_open.clicked.connect(self.click_open)

    def btnProcess(self):
        btn_open = QPushButton('PROCESS', self)
        # button.setToolTip('This is an example button')
        btn_open.move(80, 80)
        btn_open.clicked.connect(self.proses)

    # button exit
    def btnExit(self):
        btn_exit = QPushButton('EXIT', self)
        # button.setToolTip('This is an example button')
        btn_exit.move(80, 120)
        btn_exit.clicked.connect(self.click_exit)

    # Create textbox
    def texBox(self):
        self.text_show = QLineEdit(self)
        self.text_show.move(120, 20)
        self.text_show.resize(280, 40)

    def click_show(self):
        textboxValue = self.text_show.text()
        QMessageBox.question(self, 'ADAS', textboxValue,
                             QMessageBox.Ok, QMessageBox.Ok)
        self.text_show.setText("")

    def title_img_ori(self):
        title_img_ori = QLabel(self)
        title_img_ori.setText("CAPTURED IMAGE")
        title_img_ori.move(350, 40)
        title_img_ori.resize(250, 20)
        title_img_ori.setAlignment(Qt.AlignCenter)
        title_img_ori.setStyleSheet("QLabel {background-color: 'white';}")

    def label_img_ori(self):
        self.label_img_ori = QLabel(self)
        self.label_img_ori.setPixmap(QPixmap())
        self.label_img_ori.move(350, 70)
        self.label_img_ori.resize(250, 250)
        self.label_img_ori.setStyleSheet("QLabel {background-color: 'white';}")

    def title_img_hasil(self):
        self.title_img_hasil = QLabel(self)
        self.title_img_hasil.setText("IMAGE DETECTION")
        self.title_img_hasil.move(650, 40)
        self.title_img_hasil.resize(250, 20)
        self.title_img_hasil.setAlignment(Qt.AlignCenter)
        self.title_img_hasil.setStyleSheet(
            "QLabel {background-color: 'white';}")

    def label_img_hasil(self):
        self.label_img_hasil = QLabel(self)
        self.label_img_hasil.setPixmap(QPixmap())
        self.label_img_hasil.move(650, 70)
        self.label_img_hasil.resize(250, 250)
        self.label_img_hasil.setStyleSheet(
            "QLabel {background-color: 'white';}")

    def title_result(self):
        self.title_result = QLabel(self)
        self.title_result.setText("TEXT RECOGNITION")
        self.title_result.move(500, 350)
        self.title_result.resize(250, 20)
        self.title_result.setAlignment(Qt.AlignCenter)
        self.title_result.setStyleSheet(
            "QLabel {background-color: 'white';}")

    def label_result(self):
        self.label_result = QLabel(self)
        self.label_result.move(350, 380)
        self.label_result.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.label_result.resize(550, 50)
        self.title_result.setAlignment(Qt.AlignCenter)
        self.label_result.setStyleSheet("QLabel {background-color: 'white';}")

    def title_db(self):
        self.title_db = QLabel(self)
        self.title_db.setText("TEMPLATE")
        self.title_db.move(80, 330)
        self.title_db.resize(120, 20)
        self.title_db.setAlignment(Qt.AlignCenter)
        self.title_db.setStyleSheet("QLabel {background-color: 'white';}")

    def label_db(self):
        self.label_db = QLabel(self)
        self.label_db.setPixmap(QPixmap())
        self.label_db.move(80, 360)
        self.label_db.resize(120, 120)
        self.label_db.setStyleSheet("QLabel {background-color: 'white';}")

    # action click open
    def click_open(self):
        global fname
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fname, _ = QFileDialog.getOpenFileName(
        #     self, "QFileDialog.getOpenFileName()", "", "All Files (*)", options=options)

        fname, filter = QFileDialog.getOpenFileName(
            self, 'Open File', "Image Files(*)")

        if fname:
            self.loadImage(fname)

    def loadImage(self, fname):
        self.img_ori = cv2.imread(fname, 1)
        self.displayImageOri()

    def imGray(self):
        self.img_ori = cv2.imread(fname, 1)
        self.img_gray = cv2.cvtColor(self.img_ori, cv2.COLOR_BGR2GRAY)

        self.height, self.width = self.img_gray.shape[:2]
        qformat = QtGui.QImage.Format_Grayscale8

        img = QtGui.QImage(self.img_gray, self.width,
                           self.height, self.img_gray.strides[0], qformat)

        img = QPixmap.fromImage(img)
        self.label_img_hasil.setPixmap(img)
        self.label_img_hasil.setAlignment(Qt.AlignCenter)

    def displayImageOri(self):
        qformat = QImage.Format_RGB888
        self.height, self.width = self.img_ori.shape[:2]

        img = QtGui.QImage(self.img_ori.data, self.width,
                           self.height, self.img_ori.strides[0], qformat)

        img = img.rgbSwapped()

        img = QPixmap.fromImage(img)
        self.label_img_ori.setPixmap(img)
        self.label_img_ori.setAlignment(Qt.AlignCenter)

    def con_components(self, img):
        # find all your connected components (white blobs in your image)
        retval, output, stats, centroids = cv2.connectedComponentsWithStats(
            img, connectivity=8)

        # connectedComponentswithStats yields every seperated component with information on each of them, such as size
        # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
        sizes = stats[1:, -1]
        retval = retval - 1

        # minimum size of particles we want to keep (number of pixels)
        # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
        min_size = 400.0

        # your answer image
        img2 = np.zeros((output.shape))
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, retval):
            if sizes[i] >= min_size:
                img2[output == i + 1] = 255

        return img2

    def h_threshold(self, img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray_img = cv2.cvtColor(hsv_img, cv2.COLOR_BGR2GRAY)

        # equ = cv2.equalizeHist(gray_img)
        # res = np.hstack((img_A, equ))  # stacking images side-by-side

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(gray_img)

        ret, thresh1 = cv2.threshold(gray_img, 121, 255, cv2.THRESH_BINARY)

        return thresh1

    def h_morphology(self, img):
        kernel = np.ones((5, 5), np.uint8)
        # gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        mask = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        return mask

    def h_contour(self, img):
        img = img.astype(np.uint8)
        output = img.copy()
        contours, hierarchy = cv2.findContours(
            img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        mx = (0, 0, 0, 0)  # biggest bounding box so far
        mx_area = 0

        for cont in contours:
            x, y, w, h = cv2.boundingRect(cont)
            area = w*h
            if area > mx_area:
                mx = x, y, w, h
                mx_area = area
        x, y, w, h = mx

        # Output to files
        result = img[y:y+h, x:x+w]

        return result

    def mse(self, imgA, imgB):
            # the 'Mean Squared Error' between the two images is the
            # sum of the squared difference between the two images;
            # NOTE: the two images must have the same dimension

        err = np.sum((imgA.astype("float") - imgB.astype("float")) ** 2)
        err /= float(imgB.shape[0] * imgB.shape[1])

        return err

    def h_resize(self, img):
        width = 250
        height = 250
        dim = (width, height)
        img_resize = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        return img_resize

    def process_img(img):
        bilfilter = cv2.bilateralFilter(img, 9, 15, 15)

        return bilfilter

    def getListOfFiles(self, dirName):
        # create a list of file and sub directories
        # names in the given directory
        listOfFile = os.listdir(dirName)
        # listOfFile.sort(key=getListOfFiles)
        allFiles = list()

        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)

        return natsorted(allFiles)

    def hsv(img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        return hsv_img

    def gray(img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return gray_img

    def proses(self):
        self.img = cv2.imread(fname, 1)

        self.result_threshold_a = self.h_threshold(self.img)
        self.result_concom_a = self.con_components(self.result_threshold_a)
        self.result_morphology_a = self.h_morphology(self.result_concom_a)
        self.result_contour_a = self.h_contour(self.result_morphology_a)
        self.result_resize_a = self.h_resize(self.result_contour_a)

        self.dirName = 'template/fix'
        # Get the list of all files in directory tree at given path
        listOfFiles = self.getListOfFiles(self.dirName)

        index = len(listOfFiles)
        count = 0
        h_sad = []

        while count < index:
            # print(listOfFiles[count])
            # B
            img_B = cv2.imread(listOfFiles[count])
            # img_process_b = process_img(img_B)
            self.result_threshold_b = self.h_threshold(img_B)
            self.result_concom_b = self.con_components(self.result_threshold_b)
            self.result_morphology_b = self.h_morphology(self.result_concom_b)
            self.result_contour_b = self.h_contour(self.result_morphology_b)
            self.result_resize_b = self.h_resize(self.result_contour_b)

            hasil = self.mse(self.result_resize_a, self.result_resize_b)
            h_round = round(hasil)
            h_sad.append(h_round)

            count += 1

        index_image = h_sad.index(min(h_sad))
        sad_min = min(h_sad)

        # print(sad_min)
        in_image = listOfFiles[index_image]
        self.db = cv2.imread(in_image)

        self.height, self.width = self.db.shape[:2]
        qformat = QtGui.QImage.Format_RGB888

        img = QtGui.QImage(self.db, self.width,
                           self.height, self.db.strides[0], qformat)

        img = img.rgbSwapped()

        img = QPixmap.fromImage(img)
        self.label_db.setPixmap(img)
        self.label_db.setAlignment(Qt.AlignCenter)

        SIGNS_LOOKUP = {
            (0): "Belok kiri",
            (1): "Belok kanan",
            (2): "Wajib lurus",
            (4): "Dilarang lewat",
            (5): "Hati-Hati Persimpangan 4",
            (6): "Perhatian Persimpangan tiga serong",
            (7): "Perhatian hati-hati",
            (8): "Persimpangan 3"
        }

        if index_image in SIGNS_LOOKUP:
            cv2.putText(self.img, SIGNS_LOOKUP[index_image], (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 1)

            self.height, self.width = self.img.shape[:2]
            qformat = QtGui.QImage.Format_RGB888

            img = QtGui.QImage(self.img, self.width,
                               self.height, self.img.strides[0], qformat)

            img = img.rgbSwapped()

            img = QPixmap.fromImage(img)
            self.label_img_hasil.setPixmap(img)
            self.label_img_hasil.setAlignment(Qt.AlignCenter)

            self.label_result.setText(SIGNS_LOOKUP[index_image])

            mp3_fp = BytesIO()
            tts = gTTS(text=SIGNS_LOOKUP[index_image], lang='id')
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            pygame.mixer.init()
            pygame.mixer.music.load(mp3_fp)
            pygame.mixer.music.play()

        else:
            self.label_result.setText('Not Recognition')

    def click_exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exit(app.exec_())
