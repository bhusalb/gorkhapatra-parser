import cv2
from .base import BaseFilter
import core.helpers


class RemoveIfNotText(BaseFilter):
    @staticmethod
    def run(date):
        images = core.helpers.get_images_in_specific_date(date)
        for image_path in images:
            captch_ex(image_path)

    @staticmethod
    def text_detect(img, ele_size=(8, 3)):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_sobel = cv2.Sobel(img, cv2.CV_8U, 1, 0)  # same as default,None,3,1,0,cv2.BORDER_DEFAULT)
        img_threshold = cv2.threshold(img_sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
        element = cv2.getStructuringElement(cv2.MORPH_RECT, ele_size)
        img_threshold = cv2.morphologyEx(img_threshold[1], cv2.MORPH_CLOSE, element)
        contours = cv2.findContours(img_threshold, 0, 1)
        Rect = [cv2.boundingRect(i) for i in contours[1] if i.shape[0] > 100]
        RectP = [(int(i[0] - i[2] * 0.08), int(i[1] - i[3] * 0.08), int(i[0] + i[2] * 1.1), int(i[1] + i[3] * 1.1)) for
                 i in
                 Rect]
        return RectP


def captch_ex(file_name):
    img = cv2.imread(file_name)

    img_final = cv2.imread(file_name)
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    '''
            line  8 to 12  : Remove noisy portion
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
                                                         3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation

    # for cv2.x.x

    # contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    # for cv3.x.x comment above line and uncomment line below

    image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # Don't plot small false positives that aren't text
        if w < 35 and h < 35:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

        '''
        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = img_final[y :y +  h , x : x + w]

        s = file_name + '/crop_' + str(index) + '.jpg'
        cv2.imwrite(s , cropped)
        index = index + 1

        '''
    # write original image with added contours to disk
    cv2.imwrite('captcha_result.png', img)
    # cv2.waitKey(5)
