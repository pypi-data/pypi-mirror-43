import numpy

import scipy.ndimage


def gaussian_smoothing(img: numpy.ndarray, sigma) -> numpy.ndarray:
    """Applies a gaussian smoothing and returns the result."""
    sigma = (sigma,) * (len(img.shape)-1) + (0,)
    return scipy.ndimage.gaussian_filter(img, sigma)
