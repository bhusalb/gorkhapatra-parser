from filters.base import BaseFilter
import core.helpers
import cv2
from config.constants import *
import shutil


class RemoveInvalidNotices(BaseFilter):
    @staticmethod
    def run(date):
        print('Remove Invalid Notices running')
        images = core.helpers.get_images_in_specific_date(date)
        invalid_images = core.helpers.get_invalid_images()
        move_path = ROOT_DIR + '/deleted_images/' + date + '/RemoveInvalidNotices'
        for image_path in images:
            image = cv2.imread(image_path)
            for invalid_image_path in invalid_images:
                invalid_image = cv2.imread(invalid_image_path)
                diff = CompareImage.get_image_difference(image, invalid_image)
                if diff < 0.15:
                    os.makedirs(move_path, exist_ok=True)
                    shutil.copy(image_path, move_path)
                    os.remove(image_path)


class CompareImage(object):
    def __init__(self, image_1_path, image_2_path):
        self.minimum_commutative_image_diff = 1
        self.image_1_path = image_1_path
        self.image_2_path = image_2_path

    def compare_image(self):
        image_1 = cv2.imread(self.image_1_path, 0)
        image_2 = cv2.imread(self.image_2_path, 0)
        commutative_image_diff = self.get_image_difference(image_1, image_2)
        return commutative_image_diff

    @staticmethod
    def get_image_difference(image_1, image_2):
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = \
            cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff
