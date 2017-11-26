import os.path
import datetime
from config.constants import *
from core.helpers import *
from core.notification import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--date', type=str, default=str(datetime.date.today()))
parser.add_argument('--send-push-notification', type=bool, default=False)
args = parser.parse_args()

print(args)

download_single_photo.image_counter = 0
parsing_date = args.date

if not os.path.exists(ROOT_DIR + '/images/' + parsing_date) or True:
    try:
        if APP_ENV == 'production':
            send_crawling_started_message_on_slack(parsing_date)

        download_raw_images(parsing_date)
        manipulate_images(parsing_date)
        if APP_ENV == 'production':
            send_crawling_ended_message_on_slack(parsing_date)
            if args.send_push_notification:
                send_push_notification_using_fcm(parsing_date)

    except:
        print(sys.exc_info())
        if APP_ENV == 'production':
            slack.chat.post_message('#logs', '[Python Error]:' + str(sys.exc_info()))
