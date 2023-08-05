# cython: language_level=3

from libcpp.deque cimport deque
from libcpp.utility cimport pair

import numpy

cimport cython
cimport numpy


_label_dtype = numpy.int
ctypedef numpy.int_t _label_dtype_t
_edge_dtype = numpy.uint8
ctypedef numpy.uint8_t _edge_dtype_t
_rgb_dtype = numpy.uint8
ctypedef numpy.uint8_t _rgb_dtype_t
_distance_dtype = numpy.int32
ctypedef numpy.int32_t _distance_dtype_t
_visited_dtype = numpy.uint8
ctypedef numpy.uint8_t _visited_dtype_t


@cython.boundscheck(False)
@cython.wraparound(False)
def insert_edge_image(
        numpy.ndarray[_label_dtype_t, ndim=2] label_img,
        numpy.ndarray[_edge_dtype_t, ndim=2] edge_img):
    """Computes the edge image of the given label image and stores the result in edge_img. The shape of edge_img must be
    (2*s[0]-1, 2*s[1]-1), where s is label_img.shape. Only the edge pixels are set, so you probably want to initialize
    edge_img with zeros before calling this."""
    assert label_img.shape[0] > 0
    assert label_img.shape[1] > 0
    assert edge_img.shape[0] == 2*label_img.shape[0]-1
    assert edge_img.shape[1] == 2*label_img.shape[1]-1
    assert label_img.dtype == _label_dtype
    assert edge_img.dtype == _edge_dtype

    cdef int x, y, last_x, last_y
    last_x = label_img.shape[0] - 1
    last_y = label_img.shape[1] - 1
    for x in range(last_x):
        if label_img[x, last_y] != label_img[x+1, last_y]:
            edge_img[2*x+1, 2*last_y] = 1
    for y in range(last_y):
        if label_img[last_x, y] != label_img[last_x, y+1]:
            edge_img[2*last_x, 2*y+1] = 1
    for x in range(last_x):
        for y in range(last_y):
            if label_img[x, y] != label_img[x+1, y]:
                edge_img[2*x+1, 2*y] = 1
            if label_img[x, y] != label_img[x, y+1]:
                edge_img[2*x, 2*y+1] = 1
            if label_img[x, y] != label_img[x+1, y+1] or label_img[x+1, y] != label_img[x, y+1]:
                edge_img[2*x+1, 2*y+1] = 1


cdef array_equal(numpy.uint8_t* a, numpy.uint8_t* b, int n):
    """Returns True if all elements of the given arrays are equal, else False."""
    for i in range(n):
        if a[i] != b[i]:
            return False
    return True


@cython.boundscheck(False)
@cython.wraparound(False)
def insert_edge_image_rgb(
        numpy.ndarray[_rgb_dtype_t, ndim=3] img,
        numpy.ndarray[_edge_dtype_t, ndim=2] edge_img):
    """Computes the edge image of the given rgb image and stores the result in edge_img. The shape of edge_img must be
    (2*s[0]-1, 2*s[1]-1), where s is label_img.shape. Only the edge pixels are set, so you probably want to initialize
    edge_img with zeros before calling this."""
    assert img.shape[0] > 0
    assert img.shape[1] > 0
    assert edge_img.shape[0] == 2*img.shape[0]-1
    assert edge_img.shape[1] == 2*img.shape[1]-1
    assert img.dtype == _rgb_dtype
    assert edge_img.dtype == _edge_dtype

    cdef int x, y, last_x, last_y, m
    m = img.shape[2]
    last_x = img.shape[0] - 1
    last_y = img.shape[1] - 1
    for x in range(last_x):
        if not array_equal(&img[x, last_y, 0], &img[x+1, last_y, 0], m):
            edge_img[2*x+1, 2*last_y] = 1
    for y in range(last_y):
        if not array_equal(&img[last_x, y, 0], &img[last_x, y+1, 0], m):
            edge_img[2*last_x, 2*y+1] = 1
    for x in range(last_x):
        for y in range(last_y):
            if not array_equal(&img[x, y, 0], &img[x+1, y, 0], m):
                edge_img[2*x+1, 2*y] = 1
            if not array_equal(&img[x, y, 0], &img[x, y+1, 0], m):
                edge_img[2*x, 2*y+1] = 1
            if not array_equal(&img[x, y, 0], &img[x+1, y+1, 0], m) or not array_equal(&img[x+1, y, 0], &img[x, y+1, 0], m):
                edge_img[2*x+1, 2*y+1] = 1


@cython.boundscheck(False)
@cython.wraparound(False)
def _find_max_in_segment(
        int start_point_x,
        int start_point_y,
        numpy.ndarray[_distance_dtype_t, ndim=2] image,
        numpy.ndarray[_visited_dtype_t, ndim=2] visited):
    """Returns the point with the maximum value of the image segment that contains the given start_point. An image
    segment is bordered by pixels with value zero. Only considers pixels p where visited[p] is not zero. Sets visited[p]
    of all image segment pixels p to one."""
    assert image.shape[0] == visited.shape[0]
    assert image.shape[1] == visited.shape[1]

    cdef pair[int, int] current_pole
    cdef deque[pair[int, int]] points
    cdef pair[int, int] p
    cdef int width, height, current_max, px, py, x_first, x_last, y_first, y_last

    width = image.shape[0]
    height = image.shape[1]
    current_point = (start_point_x, start_point_y)
    current_max = image[start_point_x, start_point_y]
    points.push_back(current_point)
    while not points.empty():
        px = points.front().first
        py = points.front().second
        points.pop_front()
        if image[px, py] > current_max:
            current_max = image[px, py]
            current_point = (px, py)
        x_first = max(px-1, 0)
        x_last = min(px+1, width-1)
        y_first = max(py-1, 0)
        y_last = min(py+1, height-1)
        for x in range(x_first, x_last+1):
            for y in range(y_first, y_last+1):
                if not visited[x, y] and image[x, y] > 0:
                    points.push_back((x, y))
                    visited[x, y] = 1
    return current_point


@cython.boundscheck(False)
@cython.wraparound(False)
def find_max_in_all_segments(
        numpy.ndarray[_distance_dtype_t, ndim=2] image,
        numpy.ndarray[_visited_dtype_t, ndim=2] visited):
    """Returns all points that are a maximum in their image segment. An image segment is bordered by pixels with value
    zero. The arrays image and visited must have the same shape and visited must be filled with zeros."""
    assert image.shape[0] == visited.shape[0]
    assert image.shape[1] == visited.shape[1]

    cdef int x, y, px, py

    poles = []
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if not visited[x, y] and image[x, y] > 0:
                px, py = _find_max_in_segment(x, y, image, visited)
                poles.append((px-1, py-1))
    return poles
