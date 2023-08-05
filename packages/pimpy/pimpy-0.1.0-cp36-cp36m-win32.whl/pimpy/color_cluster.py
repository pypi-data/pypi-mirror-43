from typing import Tuple

import numpy
import scipy.cluster


def reduce_image(img: numpy.ndarray, k, *args, **kwargs) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Finds the k prominent colors of the given image and maps each pixel to the prominent color closest to it. Returns
    a tuple (colors, labels) where colors are the prominent colors and labels is an image that stores indices of the
    mapped colors. The expression colors[labels] gives an image with the same shape as the input image, but reduced to
    its prominent colors.
    The argument k and all additional args are not used directly and directly forwarded to the kmeans2 function."""
    original_dtype = img.dtype
    original_shape = img.shape
    img = numpy.reshape(img, (-1, original_shape[-1])).astype(numpy.float)
    centroids, labels = scipy.cluster.vq.kmeans2(img, k, *args, **kwargs)
    centroids = centroids.astype(original_dtype)
    labels_shape = original_shape[:-1]
    return centroids, numpy.reshape(labels, labels_shape)


def find_nearest_colors(img: numpy.ndarray, colors: numpy.ndarray) -> numpy.ndarray:
    """Finds the nearest color of each pixel in the given image and returns an image of the color indices. The returned
    value (labels) can be used to create a color image using colors[labels]."""
    original_shape = img.shape
    img = numpy.reshape(img, (-1, original_shape[-1]))
    labels = scipy.cluster.vq.vq(img, colors)[0]
    labels_shape = original_shape[:-1]
    return numpy.reshape(labels, labels_shape)


def extract_colors(img: numpy.ndarray) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Finds all distinct colors and returns a tuple (colors, labels) where labels is an image that stores indices of
    the mapped colors. The expression colors[labels] recreates img."""
    original_shape = img.shape
    img = numpy.reshape(img, (-1, original_shape[-1]))
    colors, labels = numpy.unique(img, axis=0, return_inverse=True)
    labels_shape = original_shape[:-1]
    return colors, numpy.reshape(labels, labels_shape)
