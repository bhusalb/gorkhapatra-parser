from .base import BaseFilter
from config.constants import *
import os
import cv2
import numpy as np
from config.constants import *
from core.geometry import Rect


class RemoveIfOverlap(BaseFilter):
    @staticmethod
    def get_valid_contours_cordinates(contours):
        contour_position = [];
        for index, cnt in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cnt)
            position = (x, y, w, h)
            if w > MIN_IMAGE_WIDTH and h > MIN_IMAGE_HEIGHT:
                contour_position.append(position)
        return contour_position

    @staticmethod
    def run(contours):
        contour_position = RemoveIfOverlap.get_valid_contours_cordinates(contours)
        overlap = []
        for position1 in contour_position:
            for position2 in contour_position:
                if not position1 == position2:
                    rect1 = Rect(position1)
                    rect2 = Rect(position2)
                    if rect1.overlaps_with(rect2):
                        if rect1.area() >= rect2.area():
                            overlap.append(position2)
                        else:
                            overlap.append(position1)

        print(overlap)
        # [contour_position.remove(overlap_index) for overlap_index in overlap]

        re = list(set(contour_position) - set(overlap))
        print(re)
        return re
