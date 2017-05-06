import numpy as np
def identify_lane_position_from_centroids(left_centroids, right_centroids, midpoint=640):
    width_of_lane = 3.7 #metres

    left_x_pos = left_centroids[0][0]
    right_x_pos = right_centroids[0][0]

    width_of_lane_in_pixels = right_x_pos - left_x_pos

    pixels_to_meter = width_of_lane_in_pixels

    distance_from_midpoint_in_pixels = midpoint - (right_x_pos - left_x_pos) / 2 + left_x_pos
    return (width_of_lane_in_pixels / width_of_lane) / distance_from_midpoint_in_pixels

def identify_lane_curviture(left_centroids, right_centroids):
    print("lane curve")

    print(left_centroids)
    ploty = np.array([centroid[1] for centroid in left_centroids])
    print(ploty)
    leftx = np.array([centroid[0] for centroid in left_centroids])
    print(leftx)
    rightx = np.array([centroid[0] for centroid in right_centroids])
    ym_per_pix = 30/720 # meters per pixel in y dimension
    xm_per_pix = 3.7/700 # meters per pixel in x dimension

    # Fit new polynomials to x,y in world space
    left_fit_cr = np.polyfit(ploty*ym_per_pix, leftx*xm_per_pix, 2)
    right_fit_cr = np.polyfit(ploty*ym_per_pix, rightx*xm_per_pix, 2)
    # Calculate the new radii of curvature
    y_eval = 700
    left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
    # Now our radius of curvature is in meters
    print(left_curverad, 'm', right_curverad, 'm')
    return left_curverad, right_curverad
    # Example values: 632.1 m    626.2 m
