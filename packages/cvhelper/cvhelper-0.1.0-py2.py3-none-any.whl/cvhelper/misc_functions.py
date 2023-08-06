from typing import Union

import cv2 as cv
import numpy as np

from .model import Point


def norm(input: Union[Point, np.ndarray]):
    """Returns the L2 norm"""
    if isinstance(input, Point):
        return cv.norm((*input,))
    else:
        return cv.norm(input)


def line_iterator(img: np.ndarray, p1: Point, p2: Point):
    """
    Produces and array that consists of the coordinates and intensities of each pixel in a line between two points.

    Credit: https://stackoverflow.com/questions/32328179/opencv-3-0-python-lineiterator

    Parameters:
        -P1: a numpy array that consists of the coordinate of the first point (x,y)
        -P2: a numpy array that consists of the coordinate of the second point (x,y)
        -img: the image being processed

    Returns:
        -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity])
    """
    # define local variables for readability
    imageH = img.shape[0]
    imageW = img.shape[1]
    # P1X = P1[0]
    # P1.y = P1[1]
    # P2X = P2[0]
    # P2.y = P2[1]

    # difference and absolute difference between points
    # used to calculate slope and relative location between points
    dX = p2.x - p1.x
    dY = p2.y - p1.y
    dXa = np.abs(dX)
    dYa = np.abs(dY)

    # predefine numpy array for output based on distance between points
    color_chls = 1 if img.ndim == 2 else 3
    itbuffer = np.empty(shape=(np.maximum(dYa, dXa), 2 + color_chls), dtype=np.int32)
    itbuffer.fill(np.nan)

    # Obtain coordinates along the line using a form of Bresenham's algorithm
    negY = p1.y > p2.y
    negX = p1.x > p2.x
    if p1.x == p2.x:  # vertical line segment
        itbuffer[:, 0] = p1.x
        if negY:
            itbuffer[:, 1] = np.arange(p1.y - 1, p1.y - dYa - 1, -1, dtype=np.int32)
        else:
            itbuffer[:, 1] = np.arange(p1.y + 1, p1.y + dYa + 1, dtype=np.int32)
    elif p1.y == p2.y:  # horizontal line segment
        itbuffer[:, 1] = p1.y
        if negX:
            itbuffer[:, 0] = np.arange(p1.x - 1, p1.x - dXa - 1, -1, dtype=np.int32)
        else:
            itbuffer[:, 0] = np.arange(p1.x + 1, p1.x + dXa + 1, dtype=np.int32)
    else:  # diagonal line segment
        # TODO: error here when drawing from bottom right to top left diagonal.
        steepSlope = dYa > dXa
        if steepSlope:
            slope = dX / dY
            if negY:
                itbuffer[:, 1] = np.arange(p1.y - 1, p1.y - dYa - 1, -1, dtype=np.int32)
            else:
                itbuffer[:, 1] = np.arange(p1.y + 1, p1.y + dYa + 1, dtype=np.int32)
            itbuffer[:, 0] = (slope * (itbuffer[:, 1] - p1.y)).astype(np.int) + p1.x
        else:
            slope = dY / dX
            if negX:
                itbuffer[:, 0] = np.arange(p1.x - 1, p1.x - dXa - 1, -1, dtype=np.int32)
            else:
                itbuffer[:, 0] = np.arange(p1.x + 1, p1.x + dXa + 1, dtype=np.int32)
            itbuffer[:, 1] = (slope * (itbuffer[:, 0] - p1.x)).astype(np.int) + p1.y

    # Remove points outside of image
    colX = itbuffer[:, 0]
    colY = itbuffer[:, 1]
    itbuffer = itbuffer[(colX >= 0) & (colY >= 0) & (colX < imageW) & (colY < imageH)]

    # Get intensities from img ndarray
    # Get three values if color image
    num_channels = 2 if img.ndim == 2 else slice(2, None, None)
    itbuffer[:, num_channels] = img[itbuffer[:, 1], itbuffer[:, 0]]

    return itbuffer
