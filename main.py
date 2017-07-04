import urllib.request, json, cv2, numpy as np, os, os.path, uuid, urllib, sys, datetime

MIN_WIDTH = 300
MIN_HIEGHT = 300
DOWNLOADED_IMAGE_PATH = os.getcwd() + '/' + "raw_images"
SAVE_IMAGE_PATH = os.getcwd() + '/' + 'images'


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


download_single_photo.image_counter = 0


def find_contours(image_path, date, page_no):
    im = cv2.imread(image_path)
    hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    COLOR_MIN = np.array([0, 0, 0], np.uint8)
    COLOR_MAX = np.array([40, 40, 40], np.uint8)
    frame_threshed = cv2.inRange(im, COLOR_MIN, COLOR_MAX)
    imgray = frame_threshed
    ret, thresh = cv2.threshold(frame_threshed, 127, 255, 0)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the index of the largest contour
    contour_position = [];
    for index, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)

        position = (x, y, w, h)

        if w > MIN_WIDTH and h > MIN_HIEGHT:
            result = is_overlapping(contour_position, position)
            print(result)
            if type(result) == int:
                contour_position[result] = position
            else:
                if result:
                    contour_position.append(position)

    # Check whether is backwhite or not
    color_boundaries = [
        ([235, 235, 235], [255, 255, 255]),
        ([0, 0, 0], [20, 20, 20])
    ]

    save_path = SAVE_IMAGE_PATH + '/' + date
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    for index, position in enumerate(contour_position):
        x, y, w, h = position
        cv2.imwrite(save_path + '/' + str(page_no) + '_' + str(index) + '.png', im[y:(y + h), x:(x + w)])


def is_overlapping(contour_position, given_position):
    for index, position in enumerate(contour_position):
        if abs(position[0] - given_position[0]) < 150 and abs(position[1] - given_position[1]) < 150:
            if position[2] < given_position[2] or position[3] < given_position[3]:
                return index
            else:
                return False

    return True


if len(sys.argv) > 1:
    parsing_date = sys.argv[0]
else:
    parsing_date = str(datetime.date.today())

crawl_data = get_json(parsing_date)

for page in crawl_data['pages']:
    download_single_photo(page['preview']['largest'], parsing_date)

path = DOWNLOADED_IMAGE_PATH + '/' + parsing_date
images = os.listdir(path)
images.sort()

for page_no,image in enumerate(images):
    find_contours(path + '/' + image, parsing_date, image.split('.')[0])
