import os
import unittest

import imageio
import numpy

from pimpy.color_cluster import extract_colors, find_nearest_colors, reduce_image


_red_blue_img = numpy.array([
    [[199, 2, 5], [10, 0, 154], [202, 4, 4], [203, 6, 1]],
    [[11, 0, 146], [13, 0, 149], [200, 0, 2], [14, 0, 151]]
], dtype=numpy.uint8)
_red_blue_img_reduced_colors = numpy.array([
    [201, 3, 3], [12, 0, 150]
], dtype=numpy.uint8)
_red_blue_img_reduced_labels = numpy.array([
    [0, 1, 0, 0],
    [1, 1, 0, 1]
])
_chelsea_img_file_path = os.path.join(os.path.dirname(__file__), "chelsea.png")
_chelsea_img = imageio.imread(_chelsea_img_file_path)
_chelsea_reduced_three_colors_img_file_path = os.path.join(os.path.dirname(__file__), "chelsea_three_colors.png")
_chelsea_reduced_three_colors_img = imageio.imread(_chelsea_reduced_three_colors_img_file_path)


class TestReduceImage(unittest.TestCase):

    def test_reduce_red_blue_img(self):
        numpy.random.seed(5)
        colors, labels = reduce_image(_red_blue_img, 2)
        self.assertTrue(numpy.array_equal(colors, _red_blue_img_reduced_colors))
        self.assertTrue(numpy.array_equal(labels, _red_blue_img_reduced_labels))

    def test_reduce_cat(self):
        numpy.random.seed(42)
        colors, labels = reduce_image(_chelsea_img, 3)
        img_reduced = colors[labels]
        self.assertTrue(numpy.array_equal(img_reduced, _chelsea_reduced_three_colors_img))


class TestFindNearestColors(unittest.TestCase):

    def test_nearest_colors_of_red_blue_image(self):
        labels = find_nearest_colors(_red_blue_img, _red_blue_img_reduced_colors)
        self.assertTrue(numpy.array_equal(labels, _red_blue_img_reduced_labels))


class TestExtractColors(unittest.TestCase):

    def test_extract_red_blue_reduced_colors(self):
        img = _red_blue_img_reduced_colors[_red_blue_img_reduced_labels]
        colors, labels = extract_colors(img)
        self.assertTrue(numpy.array_equal(colors[0], [12, 0, 150]))
        self.assertTrue(numpy.array_equal(colors[1], [201, 3, 3]))
        recreated_img = colors[labels]
        self.assertTrue(numpy.array_equal(recreated_img, img))
