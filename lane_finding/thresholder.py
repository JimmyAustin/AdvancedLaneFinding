import cv2
import numpy as np

def binarise(img, thresh_min, thresh_max):
    zeroes = np.zeros_like(img)
    zeroes[(img >= thresh_min) & (img <= thresh_max)] = 1
    return zeroes

def threshold_color(img, s_thresh_min=160, s_thresh_max=255):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s_channel = hls[:,:,2]
    return binarise(s_channel, s_thresh_min, s_thresh_max)

def threshold_sobel(img, axis='x',  thresh_min = 20, thresh_max = 100):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0) # Take the derivative in x
    abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    return binarise(scaled_sobel, thresh_min, thresh_max)

def threshold_combined_images(img):
    color = threshold_color(img)
    sobelX = threshold_sobel(img)

    combined_binary = np.zeros_like(sobelX)
    combined_binary[(color == 1) | (sobelX == 1)] = 1
    return combined_binary

def threshold_stacked_images(img):
    color = threshold_color(img)
    sobelX = threshold_sobel(img)
    print(np.average(color))
    print(np.average(sobelX))
    #sobelX = sobelX * 255
    img = np.dstack(( np.zeros_like(color), color * 255, sobelX * 255))
    return img
