from social import Facebook
import datetime
import sys
from core import notification
import argparse
from config.constants import *

parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str)
parser.add_argument('--type', type=str)

args = parser.parse_args()

print(args)

facebook = Facebook.Facebook()

try:
    if args.image and args.type:
        facebook.post_by_command(args.image, args.type)
except:
    if APP_ENV == 'production':
        notification.send_message_on_slack(str(sys.exc_info()))
