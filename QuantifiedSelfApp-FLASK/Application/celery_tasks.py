import time
from flask import session, redirect
import os
from .timestamp import *
from .models import *
from .to_csv import *
from celery import current_app as celery_inst
from .mail import *
from celery.schedules import crontab
from jinja2 import Template
from .monthly_report import *
from .graph import *

celery_inst.set_current()


@celery_inst.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=30, hour=17),  # Send a remainder every day at5.30pm IST
        send_remainder.s(), name="daily at 5:30pm"
    )
    sender.add_periodic_task(
        crontab(minute=30, hour=17, day_of_month=1),  # Send the monthly report every month at5.30pm IST
        monthly_report.s(),
        name="Monthly Report"
    )


@celery_inst.task()
def download_logsTASK(tracker_id, si_un=None):
    if si_un is not None:
        logs = None
        try:

            to_email = USER.query.filter_by(username=si_un).first().email

            tracker_type = TRACKER.query.filter_by(tracker_id=tracker_id).first().type
            if tracker_type == 'num':
                logs = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).all()

            elif tracker_type == 'bool':
                logs = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).all()

            elif tracker_type == 'time_dur':
                logs = TRACKER_TD.query.filter_by(tracker_id=tracker_id).all()

            elif tracker_type == 'mc':
                logs = TRACKER_MC.query.filter_by(tracker_id=tracker_id).all()

            filepath = log_export(tracker_type, logs)

            with open(r"templates/email_templates/download_ready.html") as file:
                temp = Template(file.read())

            sub = "[LOGS DOWNLOAD READY] LYF-RECORD: QUANTIFIED-SELF APP"
            message = temp.render(user=si_un, file_type="LOGS DATA")
            send_email(to=to_email, subject=sub, msg=message, attachment=filepath)

            return {"msg": "Successful"}, 200

        except:
            return {"msg": "Failed1"}
    else:
        return {"msg": "Failed2"}


@celery_inst.task()
def download_trackersTASK(tracker_list, si_un=None):
    if si_un is not None:
        to_email = USER.query.filter_by(username=si_un).first().email
        filepath = tracker_export(tracker_list)

        with open(r"templates/email_templates/download_ready.html") as file:
            temp = Template(file.read())

        sub = "[TRACKERS DOWNLOAD READY] LYF-RECORD: QUANTIFIED-SELF APP"
        message = temp.render(user=si_un, file_type="TRACKERS DATA")
        send_email(to=to_email, subject=sub, msg=message, attachment=filepath)

        return {"msg": "Successful"}
    else:
        return {"msg": "Failed"}


@celery_inst.task()
def send_remainder():
    users = USER.query.all()
    user_email = {user.username: [user.email, user.last_log] for user in users}
    send_reminder_to = {}

    today = current_timestamp()[:current_timestamp().index("T")]

    for k, v in user_email.items():
        if v[1].find(today) == -1:  # If the value was not logged today
            send_reminder_to[k] = v[0]

    # send_reminder_to now contains all the users who did not log to any tracker today.

    with open(r"templates/email_templates/daily_reminder.html") as file:
        temp = Template(file.read())

    for user, email_id in send_reminder_to.items():
        message = temp.render(user=user)
        sub = f"[REMAINDER] LYF-RECORD: QUANTIFIED-SELF APP"
        send_email(email_id, subject=sub, msg=message)

    return {"msg": "Successful"}


@celery_inst.task()
def monthly_report():
    users = USER.query.all()
    user_email = {user.username: user.email for user in users}

    with open(r"templates/email_templates/report_mail_temp.html") as file:
        msg_temp = Template(file.read())

    with open(r"templates/email_templates/report.html") as file:
        pdf_temp = Template(file.read())

    today = date_today().strftime('%Y-%m-%d')
    month = date_today().strftime("%B")

    done_users = []

    for user_obj in users:
        user = user_obj.username
        account_details = accountDetails(user)  # Function returns all required account details
        tracker_details = trackerDetails(user)  # Function returns a list of all trackers for the user
        all_logs = logDetails(user)

        message = msg_temp.render(user=user)
        pdf_html = pdf_temp.render(today=str(today),
                                   month=month,
                                   account_details=account_details,
                                   tracker_details=tracker_details,
                                   all_logs=all_logs,
                                   username=user
                                   )

        sub = f"[MONTHLY REPORT] LYF-RECORD: QUANTIFIED-SELF APP"

        if user not in done_users:
            pdf_path = generate_pdf(usr=user, template=pdf_html)
            send_email(to=user_obj.email, subject=sub, msg=message, attachment=pdf_path)
            done_users.append(user)

        print(f"------DONE for {user}---------")
