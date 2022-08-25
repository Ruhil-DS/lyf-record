import os

from .models import *
import datetime
from weasyprint import HTML
from .timestamp import *
import pdfkit


def accountDetails(user):
    account_details = dict()
    # ----------------------
    # Username -->
    account_details["username"] = user
    # ----------------------
    # Streak count -->
    account_details["streak"] = STREAK.query.filter_by(username=user).first().count
    # ----------------------
    # Trackers count -->
    trackers = USER_TRACKER.query.filter_by(username=user).distinct()
    tracker_count = 0
    for i in trackers:
        tracker_count += 1
    account_details["No. of trackers"] = tracker_count
    # ----------------------
    # Member since -->
    member_create = USER.query.filter_by(username=user).first()
    member_since = str(datetime.datetime.today() - datetime.datetime.strptime(member_create.creation, '%Y-%m-%d'))
    member_since = member_since.split(",")
    account_details["Member Since"] = member_since[0]
    # ----------------------
    # Last logged
    account_details["last_logged"] = USER.query.filter_by(username=user).first().last_log
    # ----------------------
    return account_details


def trackerDetails(user):
    tracker_ids = USER_TRACKER.query.filter_by(username=user).distinct()
    trackers = [TRACKER.query.filter_by(tracker_id=t_id.tracker_id).first() for t_id in tracker_ids]
    return trackers


def logDetails(user):
    tracker_ids = USER_TRACKER.query.filter_by(username=user).distinct()
    all_logs = dict()
    for tracker_obj in tracker_ids:
        logs = None
        tracker_id = tracker_obj.tracker_id
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()

        if tracker.type == 'num':
            logs = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).all()

        elif tracker.type == 'bool':
            logs = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).all()

        elif tracker.type == 'time_dur':
            logs = TRACKER_TD.query.filter_by(tracker_id=tracker_id).all()

        elif tracker.type == 'mc':
            logs = TRACKER_MC.query.filter_by(tracker_id=tracker_id).all()
        all_logs[tracker_id] = [tracker.type, logs]

    return all_logs


def generate_pdf(usr, template):
    month = date_today().strftime("%B")
    file_name = f"static/logs_download/monthly_report_{str(usr)}_{month}.pdf"
    pdfkit.from_string(template, f'{file_name}')

    return file_name

