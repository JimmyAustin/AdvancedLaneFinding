import numpy as np
def normalize_centroids(centroids):
    base = centroids[0][0] # Get x pos of first centroid
    return [(centroid[0] - base, centroid[1]) for centroid in centroids], base

def polynomialize_line(centroids, offset=0):
    x = [centroid[1] for centroid in centroids]
    y = [centroid[0] for centroid in centroids]
    p = np.polyfit(x, y, 2)
    print(p)
    equation = np.poly1d(p)
    return [(offset + equation(centroid[1]), centroid[1]) for centroid in centroids], equation

def polynomialize_centroids(left_centroids, right_centroids):
    left_centroids, left_base = normalize_centroids(left_centroids)
    right_centroids, right_base = normalize_centroids(right_centroids)

    left_centroids,l_eq = polynomialize_line(left_centroids, offset = left_base)
    right_centroids, r_eq = polynomialize_line(right_centroids, offset = right_base)
    return left_centroids, l_eq, right_centroids, r_eq
