import os
import unittest

import imageio
import numpy

from pimpy.transformations import create_edge_image, find_poles_of_inaccessibility_of_edge_image


_label_img = numpy.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [1, 2, 2, 2, 2]
])
_edge_img = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0]
], dtype=numpy.uint8)
_chelsea_smooth_file_path = os.path.join(os.path.dirname(__file__), "chelsea_smooth_three_colors.png")
_chelsea_smooth = imageio.imread(_chelsea_smooth_file_path)
_chelsea_smooth_poles = [
    (141, 831), (6, 54), (54, 94), (4, 152), (15, 191),
    (15, 355), (23, 455), (28, 528), (54, 676), (45, 847),
    (118, 30), (90, 340), (61, 157), (123, 435), (109, 209),
    (162, 470), (108, 738), (149, 701), (230, 552), (139, 763),
    (145, 619), (201, 745), (136, 202), (148, 292), (180, 156),
    (223, 361), (189, 81), (227, 831), (206, 240), (212, 304),
    (249, 453), (314, 16), (289, 153), (269, 235), (267, 583),
    (268, 670), (348, 218), (313, 357), (319, 305), (341, 789),
    (338, 696), (369, 549), (339, 57), (351, 679), (441, 861),
    (510, 30), (403, 649), (545, 143), (444, 274), (433, 391),
    (452, 374), (449, 345), (462, 704), (499, 449), (490, 368),
    (492, 638), (496, 580), (503, 263), (512, 604), (516, 364),
    (518, 786), (568, 732), (587, 787)
]


class TestCreateEdgeImage(unittest.TestCase):

    def test_create_edge_image(self):
        edges = create_edge_image(_label_img)
        self.assertTrue(numpy.array_equal(edges, _edge_img))

    def test_create_edge_image_rgb(self):
        colors = numpy.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]], numpy.uint8)
        img = colors[_label_img]
        edges = create_edge_image(img)
        self.assertTrue(numpy.array_equal(edges, _edge_img))


class TestFindPolesOfInaccessibility(unittest.TestCase):

    def test_find_poles(self):
        edges = create_edge_image(_chelsea_smooth)
        poles = find_poles_of_inaccessibility_of_edge_image(edges)
        self.assertSetEqual(set(poles), set(_chelsea_smooth_poles))
