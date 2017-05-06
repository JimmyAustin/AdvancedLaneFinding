from .rolling_average_tracker import RollingAverageTracker
import numpy as np

class CentroidFinder(object):
    def __init__(self, exclude_base_threshold = 40, window_width=50, window_height=36, margin=80):
        self.previous_l_centers = RollingAverageTracker(5)
        self.previous_r_centers = RollingAverageTracker(5)
        self.previous_left_centroids = None
        self.previous_right_centroids = None
        self.exclude_base_threshold = exclude_base_threshold
        self.window_width = window_width
        self.window_height = window_height
        self.margin = margin

    def find_bases(self, img):
        window = np.ones(self.window_width)

        l_sum = np.sum(img[int(3*img.shape[0]/4):,:int(img.shape[1]/2)], axis=0)

        if np.average(l_sum) < self.exclude_base_threshold: #Heuristic for busy bottom. Indiciates shadows or other artifacts. Ignore if their.
            l_center = np.argmax(np.convolve(window,l_sum))-self.window_width/2
            self.previous_l_centers.add(l_center)

        r_sum = np.sum(img[int(3*img.shape[0]/4):,int(img.shape[1]/2):], axis=0)

        if np.average(r_sum) < self.exclude_base_threshold: #Heuristic for busy bottom. Indiciates shadows or other artifacts. Ignore if their.
            r_center = np.argmax(np.convolve(window,r_sum))-self.window_width/2+int(img.shape[1]/2)
            self.previous_r_centers.add(r_center)

        return self.previous_l_centers.average(), self.previous_r_centers.average()

    def find_window_centroids(self, warped, smooth=True):
        l_center, r_center = self.find_bases(warped)

        left_centroids = [l_center] # Store the (left,right) window centroid positions per level
        right_centroids = [r_center] # Store the (left,right) window centroid positions per level
        window = np.ones(self.window_width) # Create our window template that we will use for convolutions

        # Go through each layer looking for max pixel locations
        for level in range(1,(int)(warped.shape[0]/self.window_height)):
            # convolve the window into the vertical slice of the image
            image_layer = np.sum(warped[int(warped.shape[0]-(level+1)*self.window_height):int(warped.shape[0]-level*self.window_height),:], axis=0)
            conv_signal = np.convolve(window, image_layer)
            # Find the best left centroid by using past left center as a reference
            # Use window_width/2 as offset because convolution signal reference is at right side of window, not center of window
            offset = self.window_width/2
            l_min_index = int(max(l_center+offset-self.margin,0))
            l_max_index = int(min(l_center+offset+self.margin,warped.shape[1]))
            subsection = conv_signal[l_min_index:l_max_index]
            if len(subsection) != 0:
                l_center = np.argmax(conv_signal[l_min_index:l_max_index])
            else:
                l_center = self.margin

            r_min_index = int(max(r_center+offset-self.margin,0))
            r_max_index = int(min(r_center+offset+self.margin,warped.shape[1]))
            subsection = conv_signal[r_min_index:r_max_index]
            if len(subsection) != 0:
                r_center = np.argmax(conv_signal[r_min_index:r_max_index])
            else:
                r_center = self.margin

            if l_center == 0 and r_center == 0:
                l_center = self.margin
                r_center = self.margin
            elif l_center == 0:
                l_center = r_center
            elif r_center == 0:
                r_center = l_center

            l_center = l_center+l_min_index-offset
            r_center = r_center+r_min_index-offset
            # Add what we found for that layer
            left_centroids.append(l_center)
            right_centroids.append(r_center)

        if smooth:
            return self.smooth_centroids(left_centroids, right_centroids)
        else:
            return left_centroids, right_centroids

    def wh_for_i(self, i):
        return (i - 1) * self.window_height + self.window_height/2

    def smooth_centroids(self, left_centroids, right_centroids):
        left_starting_point =  left_centroids[0]
        right_starting_point =  right_centroids[0]

        cl = len(left_centroids)
        #left_centroids = [left_starting_point] + [(int(level[0]),int(wh_for_i(cl-i))) for i, level in enumerate(centroids)]
        #right_centroids = [right_starting_point] + [(int(level[1]), int(wh_for_i(cl-i))) for i, level in enumerate(centroids)]
        left_centroids = [(int(level),int(self.wh_for_i(cl-i))) for i, level in enumerate(left_centroids)]
        right_centroids = [(int(level), int(self.wh_for_i(cl-i))) for i, level in enumerate(right_centroids)]
        if self.previous_left_centroids is not None:
            left_centroids, cf_left = self.mix_centroids(left_centroids, self.previous_left_centroids)
            right_centroids, cf_right = self.mix_centroids(right_centroids, self.previous_right_centroids)
        self.previous_left_centroids = left_centroids
        self.previous_right_centroids = right_centroids

        return (left_centroids, right_centroids)

    def mix_centroids(self, new_centroids,previous_centroids, mix_factor = 0.8):
        centroids = []
        change_factor = 0
        for new_point, old_point in zip(new_centroids, previous_centroids):
            x_delta = new_point[0] - old_point[0]
            change_factor = change_factor + x_delta
            x = new_point[0] - (new_point[0] - old_point[0]) * mix_factor
            y = new_point[1] - (new_point[1] - old_point[1]) * mix_factor
            centroids.append((int(x),int(y)))
        return centroids, change_factor

    def draw_window_centroids(self, warped, window_centroids):
        if len(window_centroids) > 0:
            # Points used to draw all the left and right windows
            l_points = np.zeros_like(warped)
            r_points = np.zeros_like(warped)

            # Go through each level and draw the windows
            for level in range(0,len(window_centroids)):
                # Window_mask is a function to draw window areas
                l_mask = window_mask(window_width,window_height,warped,window_centroids[level][0],level)
                r_mask = window_mask(window_width,window_height,warped,window_centroids[level][1],level)
                # Add graphic points from window mask here to total pixels found
                l_points[(l_points == 255) | ((l_mask == 1) ) ] = 128
                r_points[(r_points == 255) | ((r_mask == 1) ) ] = 255

            # Draw the results
            template = np.array(r_points+l_points,np.uint8) # add both left and right window pixels together
            zero_channel = np.zeros_like(template) # create a zero color channel
            template = np.array(cv2.merge((zero_channel,template,zero_channel)),np.uint8) # make window pixels green
            warpage = np.array(cv2.merge((warped,warped,warped)),np.uint8) # making the original road pixels 3 color channels
            output = cv2.addWeighted(warpage, 1, template, 0.5, 0.0) # overlay the orignal road image with window results

        # If no window centers found, just display orginal road image
        else:
            output = np.array(cv2.merge((warped,warped,warped)),np.uint8)
        return output
