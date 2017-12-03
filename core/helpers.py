import urllib.request, json, cv2, numpy as np, os, os.path, uuid, urllib, sys, datetime
from PIL import Image
from config.constants import *
from filters.remove_if_overlap import RemoveIfOverlap
import filters


def get_json(date):
    contents = str(
        urllib.request.urlopen("http://gorkhapatraonline.com/epaper/getdata/gorkhapatra?time=" + date).read().decode(
            "utf-8"))
    return json.loads(contents)


def download_single_photo(img_url, date):
    download_single_photo.image_counter += 1
    path = DOWNLOADED_IMAGE_PATH + '/' + date
    if not os.path.exists(path):
        os.mkdir(path)

    file_path = "%s%s%s" % (path, '/', str(download_single_photo.image_counter) + '.jpg')
    print(file_path)
    urllib.request.urlretrieve(img_url, file_path)


def generate_thumb(save_path, image_name, size=(200, 200)):
    im = Image.open(save_path + '/' + image_name)
    im.thumbnail(size)
    im.save(save_path + "/thumbs/" + image_name)


def get_gary_scale_image(image_path):
    im = cv2.imread(image_path)
    hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    COLOR_MIN = np.array([0, 0, 0], np.uint8)
    COLOR_MAX = np.array([40, 40, 40], np.uint8)
    frame_threshed = cv2.inRange(im, COLOR_MIN, COLOR_MAX)
    imgray = frame_threshed
    ret, thresh = cv2.threshold(frame_threshed, 127, 255, 0)
    return thresh


def create_directory_for_date(date):
    save_path = SAVE_IMAGE_PATH + '/' + date
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        os.mkdir(save_path + '/' + 'thumbs')


def save_images_for_date(date, image_path, contour_position, page_no):
    save_path = SAVE_IMAGE_PATH + '/' + date
    im = cv2.imread(image_path)
    for index, position in enumerate(contour_position):
        x, y, w, h = position
        image_name = str(page_no) + '_' + str(index) + '.png'
        image_path = save_path + '/' + image_name
        cv2.imwrite(image_path, im[y:(y + h), x:(x + w)])
        generate_thumb(save_path, image_name)


def find_contours(image_path, date, page_no):
    print(image_path)
    thresh = get_gary_scale_image(image_path)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the index of the largest contour

    create_directory_for_date(date)
    save_images_for_date(date, image_path, RemoveIfOverlap.run(contours), page_no)


def is_overlapping(contour_position, given_position):
    for index, position in enumerate(contour_position):
        if abs(position[0] - given_position[0]) < 10 and abs(position[1] - given_position[1]) < 10:
            if position[2] < given_position[2] or position[3] < given_position[3]:
                return index
            else:
                return False

    return True


def download_raw_images(parsing_date):
    crawl_data = get_json(parsing_date)
    for page in crawl_data['pages']:
        download_single_photo(page['preview']['largest'], parsing_date)


def get_sorted_image_list(parsing_date, full_path=False):
    path = DOWNLOADED_IMAGE_PATH + '/' + parsing_date
    images = os.listdir(path)
    if full_path:
        images = [path + '/' + image for image in images]
    images.sort()
    return images


def manipulate_images(parsing_date):
    path = DOWNLOADED_IMAGE_PATH + '/' + parsing_date
    images = get_sorted_image_list(parsing_date)
    for page_no, image in enumerate(images):
        find_contours(path + '/' + image, parsing_date, image.split('.')[0])


def get_images_count_in_specific_date(date):
    return len(get_images_in_specific_date(date))


def apply_filter(date):
    for f in FILTERS.split(','):
        obj = eval('filters.' + f)
        obj.run(date)


def get_images_in_specific_date(date):
    path = SAVE_IMAGE_PATH + '/' + date + '/'
    return [path + name for name in os.listdir(path) if
            os.path.isfile(path + name)]


def get_invalid_images():
    path = ROOT_DIR + '/' + 'invalid_images' + '/'

    return [path + name for name in os.listdir(path) if
            os.path.isfile(path + name)]
