## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[chessboard]: ./writeup_images/chessboard_undistorted.png "Chessboard"
[perspective_untransform]: ./writeup_images/untransformed_perspective.png "Untransform"
[perspective_transform]: ./writeup_images/transformed_perspective.png "Transform"
[camera_correction]: ./writeup_images/camera_correction.png "Road Transformed"

[threshold_stacked]: ./writeup_images/threshold_stacked.png "Binary Example"
[transformed_perspective]: ./writeup_images/flat_threshold.png "Binary Example"

[line_finding]: ./writeup_images/line_finding.png
[result]: ./writeup_images/result.png "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is found in lines 11-29 in `undistorter.py`. The object points are assumed to be in a fixed (x, y) plane at z=0. We generate the object points (line 12), then convert each caliration image to grayscale (line 18), find the chessboards (line 20), and add the points if the corners are found.

Once the corners are found, we calculate camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function. We then wrap the `cv2.undistort` function so that we can store the calculated data (line 31).

![alt text][chessboard]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.


To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][camera_correction]


#### 2. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warp_perspective_for_road()`, which appears in lines 6 through 8 in the file `warper.py`.  The `warper()` function takes as inputs an image.  I chose the hardcode the source and destination points in the following manner:

Src

```python
top_y = 450
top_offset = 50
bottom_y = 670
bottom_offset = 405
x_midpoint = img.shape[1]/2

left_bottom = (x_midpoint - bottom_offset, bottom_y)
left_top = (x_midpoint - top_offset, top_y)
right_top = (x_midpoint + top_offset, top_y)
right_bottom = (x_midpoint + bottom_offset, bottom_y)
```

Destination
```python
left_bottom = (250, shape[0])
left_top = (250, 0)
right_top = (shape[1]-250, 0)
right_bottom = (shape[1]-250, shape[0])
```

[[  590.   450.]
 [  690.   450.]
 [ 1045.   670.]
 [  235.   670.]]
[[  250.     0.]
 [ 1030.     0.]
 [ 1030.   720.]
 [  250.   720.]]

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 590, 450      | 250, 0        |
| 203, 450      | 1030, 0      |
| 1045, 670     | 1030, 720      |
| 235, 670      | 250, 720        |

![perspective_untransform][]

![perspective_transform][]

#### 3. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a sobel and color transform on the perspective transformed file. This is described in the `thresholder.py` file.

![threshold_stacked][]

It is flattened to a single dimension for the next stage in the pipeline.

![transformed_perspective][]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

I think used a sliding window search, with a smoothing function, and defaulting to using the same offset as the opposing side if a suitable result can not be found, in order to select 2 series of points that can then be fitted to a 2nd order polynomial.

![line_finding][]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

Lane position was calculated by assuming that the camera is mounted to the exact center of the car, the lane is 3.7m wide. I used the bottom of the two curves, and compared their midpoint with the midpoint of the middle. This was then used to calculate the location of the car, which appears to be roughly 30cm off the midpoint. This was caluclated in `lane_position_finder.py`, lines 2-13

Lane curvature was calculated using the code from the udacity tutorial, which can also be found in `lane_position_finder.py` , lines 15-37.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

The overall combination was done in an Jupyter notebook. A sample output looks like this.

![result][result]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](https://youtu.be/K-n4Jr0If3g)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

This pipeline will likely fail during lane changes, merges, or splits. It will also likely fail in poor weather, or where shadows are involved.

For future improvements I would focus on improving the thresholding section. 
