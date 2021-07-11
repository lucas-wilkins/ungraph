""" This deals with transformations between image and data coordinates"""

from typing import List, Tuple

import numpy as np

#
# The transform is of the form
#
#    data = R.im + T
#
# and it must satisfy
#
#  (im_x0_x, im_x0_y) -> (x0, cx)
#  (im_x1_x, im_x1_y) -> (x1, cx)
#  (im_y0_x, im_y0_y) -> (cy, y0)
#  (im_y1_x, im_y1_y) -> (cy, y1)
#
# Where cx and cy are unknown axis offsets
#
# So, there are
#   four unknowns for rotation and scaling
#   two unknowns for the translation
#   and two unknowns for the axes offsets
#
#
#

class Transform:
    def __init__(self, x_axis: List[Tuple[float, float]], x0, x1, y_axis: List[Tuple[float, float]], y0, y1):

        x0x = x_axis[0][0]
        x0y = x_axis[0][1]
        x1x = x_axis[1][0]
        x1y = x_axis[1][1]
        y0x = y_axis[0][0]
        y0y = y_axis[0][1]
        y1x = y_axis[1][0]
        y1y = y_axis[1][1]

        denom = (x0y - x1y) * (y0x - y1x) - (x0x - x1x) * (y0y - y1y)

        a = -(x0 - x1) * (y0y - y1y) / denom
        b = (x0 - x1) * (y0x - y1x) / denom
        c = (x0y - x1y) * (y0 - y1) / denom
        d = -(x0x - x1x) * (y0 - y1) / denom

        x_offset = x0y * x1 * (y0x - y1x) + x0x * x1 * (-y0y + y1y) +  \
                   x0 * (-x1y * y0x + x1x * y0y + x1y * y1x - x1x * y1y)
        x_offset /= denom

        y_offset = x0y *y0x *y1 - x1y *y0x* y1 - x0x *y0y *y1 + x1x *y0y* y1 - \
                   x0y* y0 *y1x + x1y* y0 *y1x + (x0x - x1x)* y0 *y1y
        y_offset /= denom

        self.translation = np.array([x_offset, y_offset])
        self.mult = np.array([[a, b], [c, d]]).T

    def __call__(self, xy):
        return np.dot(np.array(xy), self.mult) + self.translation