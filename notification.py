from core.notification import send_push_notification_using_fcm
import datetime

notification_date = str(datetime.date.today())
send_push_notification_using_fcm(notification_date)
