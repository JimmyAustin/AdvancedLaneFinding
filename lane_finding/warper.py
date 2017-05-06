import cv2
import numpy as np
import scipy

def warp_perspective_for_road(img):
    M = cv2.getPerspectiveTransform(vertices(img), destination_vertices(img))
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
    return warped#scipy.misc.imfilter(warped, 'edge_enhance')

def vertices(img, closed = False,dtype=np.float32):
    top_y = 450
    top_offset = 50
    bottom_y = 670
    bottom_offset = 405
    x_midpoint = img.shape[1]/2

    left_bottom = (x_midpoint - bottom_offset, bottom_y)
    left_top = (x_midpoint - top_offset, top_y)
    right_top = (x_midpoint + top_offset, top_y)
    right_bottom = (x_midpoint + bottom_offset, bottom_y)

    if closed:
        return np.array([left_top, right_top, right_bottom, left_bottom, left_top], dtype=dtype)
    else:
        return np.array([left_top, right_top, right_bottom, left_bottom], dtype=dtype)

def destination_vertices(img, closed = False,dtype=np.float32):
    shape = img.shape
    left_bottom = (250, shape[0])
    left_top = (250, 0)
    right_top = (shape[1]-250, 0)
    right_bottom = (shape[1]-250, shape[0])

    if closed:
        return np.array([left_top, right_top, right_bottom, left_bottom, left_top], dtype=dtype)
    else:
        return np.array([left_top, right_top, right_bottom, left_bottom], dtype=dtype)

def merge_line_image_and_image(img, line_image, α=0.8, β=0.3, λ=0.):
    r_M = cv2.getPerspectiveTransform(destination_vertices(img), vertices(img))
    line_image_s = (line_image.shape[1], img.shape[0])
    r_line_image = cv2.warpPerspective(line_image, r_M, line_image_s, flags=cv2.INTER_LINEAR)
    return cv2.addWeighted(img, α, r_line_image, β, λ)
