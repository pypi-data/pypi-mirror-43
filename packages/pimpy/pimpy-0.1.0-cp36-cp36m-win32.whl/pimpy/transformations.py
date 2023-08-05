from typing import List, Tuple

import numpy
import scipy.ndimage.morphology

from pimpy_c import find_max_in_all_segments, insert_edge_image, insert_edge_image_rgb


Point = Tuple[int, int]


def create_edge_image(label_img: numpy.ndarray) -> numpy.ndarray:
    """Returns the edge image of the given label image. The edge image has the shape (2*w-1, 2*h-1) where (w, h) are
    width and height of the given image. A pixel of the edge image has value 1 if it is an edge and value 0 if it is a
    background pixel."""
    n_dim = len(label_img.shape)
    assert n_dim in (2, 3)
    edges = numpy.zeros((2*label_img.shape[0]-1, 2*label_img.shape[1]-1), dtype=numpy.uint8)
    if n_dim == 2:
        insert_edge_image(label_img, edges)
    elif n_dim == 3:
        insert_edge_image_rgb(label_img, edges)
    return edges


def find_poles_of_inaccessibility_of_edge_image(input_edge_img: numpy.ndarray) -> List[Point]:
    """Returns all poles of inaccessibility of the given edge image."""
    assert len(input_edge_img.shape) == 2
    assert input_edge_img.dtype == numpy.uint8
    shape = (input_edge_img.shape[0]+2, input_edge_img.shape[1]+2)
    bordered_edge_img = numpy.zeros(shape, dtype=numpy.uint8)
    bordered_edge_img[1:shape[0]-1, 1:shape[1]-1] = 1-input_edge_img
    distances = scipy.ndimage.morphology.distance_transform_cdt(bordered_edge_img)
    visited = numpy.zeros(shape, numpy.uint8)
    return find_max_in_all_segments(distances, visited)
