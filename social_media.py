from social import Facebook
import datetime
import sys
from core import notification
import argparse
from config.constants import *

parser = argparse.ArgumentParser()
parser.add_argument('--date', type=str, default=str(datetime.date.today() - datetime.timedelta(days=1)))

args = parser.parse_args()

print(args)

facebook = Facebook.Facebook()


try:
    facebook.post(args.date)
except:
    if APP_ENV == 'production':
        notification.send_message_on_slack(str(sys.exc_info()))
