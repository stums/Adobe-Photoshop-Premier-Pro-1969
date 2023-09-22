#create the Easy Editor photo editor here!
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter
import os

#
app = QApplication([])
main = QWidget()
main.setWindowTitle("Adobe Photoshop Pro")
main.resize(1000,600)
#
folder = QPushButton("Open Folder")
photo = QListWidget()
image_text = QLabel("image wil aper hee...")
#
left = QPushButton("Rotate Left")
right = QPushButton("Rotate Right")
color = QPushButton("Saturation")
contrast = QPushButton("Smooth")
blur = QPushButton("Blur")
gray = QPushButton("Gray")
mirror = QPushButton("Mirror")
sharp = QPushButton("Sharpen")
#
master = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()

col1.addWidget(folder)
col1.addWidget(photo)

row1.addWidget(left)
row1.addWidget(right)
row1.addWidget(color)
row1.addWidget(contrast)

row2.addWidget(blur)
row2.addWidget(gray)
row2.addWidget(mirror)
row2.addWidget(sharp)

col2.addWidget(image_text)
col2.addLayout(row1)
col2.addLayout(row2)


master.addLayout(col1,20)
master.addLayout(col2,80)
main.setLayout(master)






workdir = ""


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(filenames, extensions):
    results = []
    for file in filenames:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results

def showFiles():
    extensions = [".jpg",".png","jpeg","svg"]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    photo.clear()

    for file in filenames:
        photo.addItem(file)



folder.clicked.connect(showFiles)


class ImageEditor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.edit = "/save_folder"

    def loadImage(self,directory,filename):
        self.directory = directory
        self.filename = filename
        image_path = os.path.join(self.directory,self.filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        image_text.hide()
        my_pic = QPixmap(path)
        w, h = image_text.width(), image_text.height()
        my_pic = my_pic.scaled(w,h,Qt.KeepAspectRatio)
        image_text.setPixmap(my_pic)
        image_text.show()

    def saveImage(self):
        path = os.path.join(workdir, self.edit)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def gray(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def color(self):
        self.image = ImageEnhance.Color(self.image).enhance(10)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def contrast(self):
        self.image = self.image.filter(ImageFilter.SMOOTH)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def upside_down(self):
        self.image = self.image.transpose(Image.ROTATE_180)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir,self.edit,self.filename)
        self.showImage(image_path)


def displayImage():
    if photo.currentRow() >=0:
        filename = photo.currentItem().text()
        myapp.loadImage(workdir, filename)
        path = os.path.join(myapp.directory, myapp.filename)
        myapp.showImage(path)


myapp = ImageEditor()
photo.currentRowChanged.connect(displayImage)
gray.clicked.connect(myapp.gray)
left.clicked.connect(myapp.left)
right.clicked.connect(myapp.right)
color.clicked.connect(myapp.color)
contrast.clicked.connect(myapp.contrast)
blur.clicked.connect(myapp.blur)
mirror.clicked.connect(myapp.mirror)
sharp.clicked.connect(myapp.sharpen)











main.show()
app.exec_()