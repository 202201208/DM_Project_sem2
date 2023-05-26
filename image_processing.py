import cv2
import numpy as np

def apply_kernal(img, mat, dest):
    mat = np.array(mat)
    final_img = cv2.filter2D(src=img, ddepth=-1, kernel=mat)
    cv2.imwrite(dest, final_img)
    
