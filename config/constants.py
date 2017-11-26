import os.path
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.join(os.path.dirname(__file__), '../'))
DOWNLOADED_IMAGE_PATH = ROOT_DIR + '/' + 'raw_images'
SAVE_IMAGE_PATH = ROOT_DIR + '/' + 'images'

# input from env file
load_dotenv(ROOT_DIR + '/.env')

MIN_IMAGE_WIDTH = int(os.getenv('MIN_IMAGE_WIDTH'))
MIN_IMAGE_HEIGHT = int(os.getenv('MIN_IMAGE_HEIGHT'))
SLACK_API_KEY = os.getenv('SLACK_API_KEY')
FILTERS = os.getenv('FILTERS')
FIRE_BASE_API_KEY = os.getenv('FIRE_BASE_API_KEY')
PUSH_NOTIFICATION_MESSAGE_NP = os.getenv('PUSH_NOTIFICATION_MESSAGE_NP')
PUSH_NOTIFICATION_MESSAGE_EN = os.getenv('PUSH_NOTIFICATION_MESSAGE_EN')
APP_ENV = os.getenv('APP_ENV')
