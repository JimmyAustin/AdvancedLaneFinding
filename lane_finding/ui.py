import cv2

def add_lane_position_and_curve_to_img(img, lane_position, curve):
    cv2.putText(img,"{0}m off center".format(round(lane_position,2)), (0,50), cv2.FONT_HERSHEY_TRIPLEX, 2, 255, thickness=8)
    cv2.putText(img,"{0}m".format(round(curve,2)), (0,150), cv2.FONT_HERSHEY_TRIPLEX, 2, 255, thickness=8)
    return img
