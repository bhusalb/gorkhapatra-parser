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

log = {'date': parsing_date,
       'crawl_status': 'fail',
       'logged_time': None,
       'download_count': 0,
       'err': None
       }

check_log_file_if_crawl_successfully_or_not(parsing_date)

if not check_log_file_if_crawl_successfully_or_not(parsing_date) or APP_ENV == 'testing':
    try:
        if APP_ENV == 'production':
            send_crawling_started_message_on_slack(parsing_date)

        download_raw_images(parsing_date)
        manipulate_images(parsing_date)
        apply_filter(parsing_date)
        if APP_ENV == 'production':
            send_crawling_ended_message_on_slack(parsing_date)
            if args.send_push_notification:
                send_push_notification_using_fcm(parsing_date)

        log['crawl_status'] = 'success'
        log['download_count'] = get_images_count_in_specific_date(parsing_date)
        log_crawl_status_locally(log)
    except:
        print(sys.exc_info())
        log['err'] = str(sys.exc_info())
        log_crawl_status_locally(log)
        if APP_ENV == 'production':
            slack.chat.post_message('#logs', '[Python Error]:' + str(sys.exc_info()))
