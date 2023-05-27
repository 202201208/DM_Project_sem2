import cv2
import numpy as np
from PIL import Image, ImageFilter

def apply_kernal(img, mat, dest):
    mat = np.array(mat)
    final_img = cv2.filter2D(src=img, ddepth=-1, kernel=mat)
    cv2.imwrite(dest, final_img)
    
def scale_img(img, fx, fy, path):
  final_img = cv2.resize(img, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
  cv2.imwrite(path, final_img)

def resize_img(img, width, height, path):
  final_img = cv2.resize(img, (width, height))
  cv2.imwrite(path, final_img)

def translate_img(img, tx, ty, path):
  M = np.float32([[1,0,tx],[0,1,ty]])
  dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]))
  cv2.imwrite(path, dst)

def rotate_img(img, x, y, deg, scale, path):
  height, width = img.shape[:2]
  matrix = cv2.getRotationMatrix2D((x,y), deg, scale)
  translated = cv2.warpAffine(img, matrix, (width, height))
  cv2.imwrite(path, translated)

def shearing_img(img, sx, sy, path):
  height, width = img.shape[:2]
  M = np.float32([[1, sx, 0], [sy, 1, 0], [0, 0, 1]])
  sheared_img = cv2.warpPerspective(img, M, (int(width*2), int(height*2)))
  cv2.imwrite(path, sheared_img)

def reflecting_img(img, f, path):
  final_img = cv2.flip(img, f)
  cv2.imwrite(path, final_img)

def negative_img(img, path):
  height, width, _ = img.shape
  for i in range(0, height - 1):
    for j in range(0, width - 1):
        a = img.item(i, j, 0)
        b = img.item(i, j, 1)
        c = img.item(i, j, 2)
        img.itemset((i, j, 0) , 255-a)
        img.itemset((i, j, 1) , 255-b)
        img.itemset((i, j, 2) , 255-c)
  cv2.imwrite(path, img)

def logtransformation_img(img, path):
  c = 255 / np.log(1 + np.max(img))
  log_img = c * (np.log(img + 1))
  log_img = np.array(log_img, dtype=np.uint8)
  cv2.imwrite(path, log_img)

def gammatransformation_img(img, g, path): 
  log_img = np.array(255*(img / 255) ** g, dtype=np.uint8)
  cv2.imwrite(path, log_img)

def gaussianfilter_img(opath, path): 
  img = Image.open(opath)
  image = img.filter(ImageFilter.GaussianBlur)
  image.save(path)

def medianfilter_img(opath, path): 
  img = Image.open(opath)
  image = img.filter(ImageFilter.MedianFilter(size = 3))
  image.save(path)

def minfilter_img(opath, path): 
  img = Image.open(opath)
  image = img.filter(ImageFilter.MinFilter(size = 3))
  image.save(path)

def maxfilter_img(opath, path): 
  img = Image.open(opath)
  image = img.filter(ImageFilter.MaxFilter(size = 3))
  image.save(path)

def cannyedgedetector_img(img, l, u, a, path):
  edge = cv2.Canny(img, l, u, apertureSize=a)
  cv2.imwrite(path, edge)