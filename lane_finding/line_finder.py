from .centroid_finder import CentroidFinder
import numpy as np
import cv2
from .lane_position_finder import identify_lane_position_from_centroids, identify_lane_curviture
from .line_fitter import *
from .rolling_average_tracker import RollingAverageTracker

class LineFinder(object):
    def __init__(self):
        self.centroid_finder = CentroidFinder()
        self.curve_tracker = RollingAverageTracker(10)
    def identify_lines(self, img, draw_change_factor=False):
        left_centroids, right_centroids = self.centroid_finder.find_window_centroids(img, smooth=True)

        img = np.dstack(( img, np.zeros_like(img), np.zeros_like(img)))

        left_centroids, left_equation, right_centroids, right_equation = polynomialize_centroids(left_centroids, right_centroids)

        draw_line_of_points(left_centroids, img)
        draw_line_of_points(right_centroids, img)

        all_points = np.int_([np.concatenate((left_centroids,np.flipud(right_centroids)))])
        cv2.fillPoly(img, all_points, (128,128, 0))

        lane_position = identify_lane_position_from_centroids(left_centroids, right_centroids)

        left_curve, right_curve = identify_lane_curviture(left_centroids, right_centroids)

        self.curve_tracker.add(left_curve)

        return img, lane_position, self.curve_tracker.average()

def draw_line_of_points(points, line_image, color = (255,0,255)):
    previous_point = None
    for point in points:
        point = (int(point[0]), int(point[1]))
        if previous_point is None:
            previous_point = point
            continue
        cv2.arrowedLine(line_image, previous_point, point, color, 10)
        previous_point = point
