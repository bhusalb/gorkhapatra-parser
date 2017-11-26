from slacker import Slacker
from config.constants import *
from pyfcm import FCMNotification
from .helpers import get_images_count_in_specific_date

slack = Slacker(SLACK_API_KEY)
push_service = FCMNotification(api_key=FIRE_BASE_API_KEY)


def send_crawling_started_message_on_slack(parsing_date):
    slack.chat.post_message('#logs', '[Python]: Crawling Started for ' + parsing_date)


def send_crawling_ended_message_on_slack(parsing_date):
    slack.chat.post_message('#logs',
                            '[Python]: Crawling Completed for '
                            + parsing_date + ' \n total notices: ' + str(
                                get_images_count_in_specific_date(parsing_date)))


def send_push_notification_using_fcm(date):
    notice_count = get_images_count_in_specific_date(date)
    if notice_count:
        push_service.notify_topic_subscribers(topic_name="notices", message_body={
            'en': {
                'alert_title': 'Notices',
                'alert_message': PUSH_NOTIFICATION_MESSAGE_EN % (str(notice_count)),
            },
            'np': {
                'alert_title': 'सूचनाहरू',
                'alert_message': PUSH_NOTIFICATION_MESSAGE_NP % (str(notice_count)),
            }
        })
