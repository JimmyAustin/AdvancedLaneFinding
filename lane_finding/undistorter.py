import cv2
import numpy as np

class Undistorter(object):
    spec_func = 1234

    def __init__(self, calibration_images):
        self.mtx, self.dist = Undistorter.get_undistort_matrix(calibration_images)

    def get_undistort_matrix(calibration_images, ny=6, nx=9):
        objp = np.zeros((ny*nx,3), np.float32)
        objp[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1,2).astype('float32')

        objpoints = []
        imgpoints = []

        for img in calibration_images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

        img_size = (calibration_images[0].shape[1], calibration_images[1].shape[0])

        _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)

        return mtx, dist

    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
