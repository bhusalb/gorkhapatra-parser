from filters.base import BaseFilter
import core.helpers
import cv2
from config.constants import *
import shutil


class RemoveFaces(BaseFilter):
    @staticmethod
    def run(date):
        images = helpers.get_images_in_specific_date(date)
        faceCascade = cv2.CascadeClassifier(ROOT_DIR + '/opencv-files/frontalface.xml')
        eyeCascade = cv2.CascadeClassifier(ROOT_DIR + '/opencv-files/eye.xml')
        movePath = ROOT_DIR + '/deleted-images/' + date + '/RemoveFaces'
        for imagePath in images:
            image = cv2.imread(imagePath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray)
            eyes = eyeCascade.detectMultiScale(gray)

            print('faces count %s and eyes count %s' % (len(faces), len(eyes)))
            if len(faces) > 0 and len(eyes) > 0:
                os.makedirs(movePath, exist_ok=True)
                shutil.copy(imagePath, movePath)
                os.remove(imagePath)
