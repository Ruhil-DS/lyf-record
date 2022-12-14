from flask_restful import Resource, reqparse
from flask import session, redirect, jsonify
from .models import *
from .timestamp import *
import datetime
from flask import request, redirect
from flask import session, url_for
from flask import current_app as app
from .controller_index import *
from .graph import *
from .to_csv import *
import matplotlib.pyplot as plt
import os
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from .cache_instance import current_cache_inst as cache
from .ApiFunctions.allApiFunctions import *
from .celery_tasks import *


class LoginAPI(Resource):
    def post(self):

        login_parser = reqparse.RequestParser()

        # signin parameters added to the parser
        login_parser.add_argument('username')
        login_parser.add_argument('password')

        args = login_parser.parse_args()
        si_un = args.get('username', None).lower()
        si_ps = args.get('password', None)

        validity = USER.query.filter_by(username=si_un, password=si_ps).first()

        if validity is not None:
            session['username'] = si_un  # Storing sign-in username in the session!

            # Handling streak for the user
            streak_data = STREAK.query.filter_by(username=si_un).first()
            # If difference has '1 day' in it, then ->
            if '1 day' in str(datetime.datetime.today() - datetime.datetime.strptime(streak_data.date, '%Y-%m-%d')):
                streak_data.date = datetime.date.today()
                streak_data.count += 1  # Add 1 to last streak count
                db.session.commit()
            # else if difference has 'days' in it, then the streak has been broken. So ->
            elif 'days' in str(
                    datetime.datetime.today() - datetime.datetime.strptime(streak_data.date, '%Y-%m-%d')):
                streak_data.date = datetime.date.today()
                streak_data.count = 1  # Reset to 1
                db.session.commit()
            else:
                pass
            access_token = create_access_token(identity=si_un, expires_delta=datetime.timedelta(hours=5))
            return {"access_token": access_token}, 200  # After updating streak, give success response and token

        elif validity is None:  # If validity fails, give failed response
            return {"access_token": "Failed"}, 406


class SignupAPI(Resource):
    def post(self):
        signup_parser = reqparse.RequestParser()
        # signup parameters added to the parser
        signup_parser.add_argument('username')
        signup_parser.add_argument('password')
        signup_parser.add_argument('email')
        args = signup_parser.parse_args()

        su_un = args.get("username", None).lower()
        su_ps = args.get("password", None)
        su_email = args.get("email", None)

        # Creation_date() function from timestamp.py, returns today's date
        creation_date = date_today()

        try:  # Try to add a user to the db
            if su_un.strip() == "":
                raise Exception("Username can't be empty")
            new_user = USER(username=su_un, password=su_ps, email=su_email, creation=creation_date)
            streak_data = STREAK(username=su_un, date=date.today(), count=1)
            db.session.add(new_user)
            db.session.add(streak_data)
            db.session.commit()
        except:  # if anything fails, it renders the signup page with an error
            db.session.rollback()  # Roll-back just in case anything was changed
            return {"signup": "Failed"}, 406

        return {"signup": "Successful"}, 200
        # it renders the signin/up page with a message saying successful signup


class DashboardAPI(Resource):
    @jwt_required()
    def get(self):
        si_un = get_jwt_identity()
        result = getDashboardDetails(si_un=si_un)  # Cached result
        return result


class trackersAPI(Resource):
    @jwt_required()
    def get(self):
        si_un = get_jwt_identity()
        results = getTrackerDetails(si_un)  # Cached Results
        return results

    @jwt_required()
    def post(self):
        si_un = get_jwt_identity()
        # If post request, delete all cache
        cache.delete_memoized(getDashboardDetails, si_un)
        cache.delete_memoized(getTrackerDetails, si_un)
        cache.delete_memoized(getTrackerInfo, si_un)
        cache.delete_memoized(getLogInfo, si_un)

        if si_un:
            create_tracker_parser = reqparse.RequestParser()
            create_tracker_parser.add_argument("tracker_name")
            create_tracker_parser.add_argument("tracker_type")
            create_tracker_parser.add_argument("tracker_desc")
            create_tracker_parser.add_argument("mc_choices")
            args = create_tracker_parser.parse_args()

            try:
                tracker_name = args.get("tracker_name", None)
                tracker_type = args.get("tracker_type", None)
                tracker_desc = args.get("tracker_desc", None)

                tracker_record = TRACKER(name=tracker_name, description=tracker_desc, type=tracker_type)
                db.session.add(tracker_record)
                # db.session.commit()

                if tracker_type == 'mc':
                    # -----------------------
                    # When the tracker type is multi choice, add those choices to the MULTI_CHOICE table
                    # ----------------------
                    mc_choices = args.get("mc_choices", None)

                    if mc_choices is None:
                        db.session.rollback()
                        return {"Creation": "Failed"}, 400
                    db.session.commit()
                    mc_record = MULTI_CHOICES(tracker_id=tracker_record.tracker_id, choices=mc_choices)
                    db.session.add(mc_record)

                db.session.commit()

                # ----------------------
                # Link the user with the tracker ID in the USER_TRACKER table
                # ----------------------
                user_tracker_record = USER_TRACKER(username=si_un, tracker_id=tracker_record.tracker_id)

                db.session.add(user_tracker_record)
                db.session.commit()
                return {"creation": "Successful"}

            except:
                # ----------------------
                # If by any chance, something goes wrong(on the user or client side), this throws an error!
                # ----------------------
                return {"Creation": "Failed"}, 404
        else:
            return {"Message": "Failed to perform the action"}, 400

    @jwt_required()
    def patch(self, tracker_id):
        si_un = get_jwt_identity()
        # If patch request, delete all cache
        cache.delete_memoized(getDashboardDetails, si_un)
        cache.delete_memoized(getTrackerDetails, si_un)
        cache.delete_memoized(getLogDetails, si_un, tracker_id)
        cache.delete_memoized(getTrackerInfo, si_un, tracker_id)
        cache.delete_memoized(getLogInfo, si_un, tracker_id)

        if si_un:

            choices = ""

            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
            # if tracker.type == 'mc':
            #     choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
            #     choices = choices_record.choices.split(",")

            update_tracker_parser = reqparse.RequestParser()
            update_tracker_parser.add_argument("tracker_name_updated")
            update_tracker_parser.add_argument("tracker_desc_updated")
            args = update_tracker_parser.parse_args()

            tracker_name = args.get('tracker_name_updated', None)
            tracker_desc = args.get('tracker_desc_updated', None)

            print("--------------------------")
            print("--------------------------")
            print(f"tracker_name -> {tracker_name}, tracker_desc --> {tracker_desc}")
            print("--------------------------")
            print("--------------------------")

            old_record = TRACKER.query.filter_by(tracker_id=tracker_id).first()
            if tracker_name is not None:
                old_record.name = tracker_name
                old_record.description = tracker_desc
            db.session.commit()

            if tracker_name is None:
                return {"Update": "Failed"}, 400

            return {"Update": "Successful"}

        else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
            return {"Message": "Login Required"}, 400

    @jwt_required()
    def delete(self, tracker_id):
        si_un = get_jwt_identity()

        # If delete request, delete all cache
        cache.delete_memoized(getDashboardDetails, si_un)
        cache.delete_memoized(getTrackerDetails, si_un)
        cache.delete_memoized(getLogDetails, si_un, tracker_id)
        cache.delete_memoized(getTrackerInfo, si_un, tracker_id)
        cache.delete_memoized(getLogInfo, si_un, tracker_id)

        if si_un:

            try:
                tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
                if tracker.type == 'num':
                    try:
                        records = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).delete()
                    except:
                        pass
                    user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    db.session.commit()

                elif tracker.type == 'bool':
                    try:
                        records = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).delete()
                    except:
                        pass
                    user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    db.session.commit()

                elif tracker.type == 'mc':
                    try:
                        records = TRACKER_MC.query.filter_by(tracker_id=tracker_id).delete()
                        mc_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).delete()
                    except:
                        pass
                    user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    db.session.commit()

                else:
                    try:
                        records = TRACKER_TD.query.filter_by(tracker_id=tracker_id).delete()
                    except:
                        pass
                    user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
                    db.session.commit()

                return {"Deletion": "Successful"}
            except:
                return {"Deletion": "Failed"}, 400

        else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
            return {"message": "Login required."}, 400


class logSpecificAPI(Resource):
    @jwt_required()
    def get(self, tracker_id):
        si_un = get_jwt_identity()
        results = getLogDetails(si_un, tracker_id)  # Cached results
        return results

    @jwt_required()
    def post(self, tracker_id):
        si_un = get_jwt_identity()

        # If post request, delete all cache
        cache.delete_memoized(getDashboardDetails, si_un)
        cache.delete_memoized(getTrackerDetails, si_un)
        cache.delete_memoized(getLogDetails, si_un, tracker_id)
        cache.delete_memoized(getTrackerInfo, si_un, tracker_id)
        cache.delete_memoized(getLogInfo, si_un, tracker_id)
        if si_un:
            add_log_parser = reqparse.RequestParser()
            add_log_parser.add_argument("note")
            add_log_parser.add_argument("timestamp")
            add_log_parser.add_argument("value")
            add_log_parser.add_argument("start_val")
            add_log_parser.add_argument("end_val")
            add_log_parser.add_argument("choice_list")
            args = add_log_parser.parse_args()

            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
            timestamp = args.get('timestamp', None)
            note = args.get('note', None)

            if tracker.type == 'num':
                tracker_value = args.get('value')
                if note is not None:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value, note=note)
                else:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value)
                db.session.add(record)
                db.session.commit()

            elif tracker.type == 'time_dur':
                tracker_value_start = args.get('start_val')
                tracker_value_end = args.get('end_val')
                if note is not None:
                    record = TRACKER_TD(tracker_id=tracker_id, timestamp=timestamp,
                                        note=note, time_start=tracker_value_start,
                                        time_end=tracker_value_end)
                else:
                    record = TRACKER_TD(tracker_id=tracker_id, timestamp=timestamp,
                                        time_start=tracker_value_start,
                                        time_end=tracker_value_end)
                db.session.add(record)
                db.session.commit()

            elif tracker.type == 'bool':
                tracker_value = args.get('value')
                if note is not None:
                    record = TRACKER_BOOL(tracker_id=tracker_id, timestamp=timestamp,
                                          value=tracker_value, note=note)
                else:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value)
                db.session.add(record)
                db.session.commit()

            elif tracker.type == 'mc':
                # tracker_values_list = args.get('choice_list').split(",")
                tracker_value = args.get('choice_list')

                # for i in range(len(tracker_values_list)):
                #     if i != len(tracker_values_list) - 1:
                #         tracker_value += str(tracker_values_list[i]) + ","
                #     else:
                #         tracker_value += str(tracker_values_list[i])

                if note is not None:
                    record = TRACKER_MC(tracker_id=tracker_id, timestamp=timestamp,
                                        value=tracker_value, note=note)
                else:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value)
                db.session.add(record)
                db.session.commit()
            tracker.last_log = timestamp
            db.session.commit()

            return {"Logging": "Successful"}

        else:
            return {"Message": "Login required."}, 400

    @jwt_required()
    def patch(self, tracker_id, log_id):
        si_un = get_jwt_identity()

        # If patch request, delete all cache
        cache.delete_memoized(getDashboardDetails, si_un)
        cache.delete_memoized(getTrackerDetails, si_un)
        cache.delete_memoized(getLogDetails, si_un, tracker_id)
        cache.delete_memoized(getTrackerInfo, si_un, tracker_id)
        cache.delete_memoized(getLogInfo, si_un, tracker_id)
        if si_un:

            update_log_parser = reqparse.RequestParser()
            update_log_parser.add_argument("note")
            update_log_parser.add_argument("timestamp")
            update_log_parser.add_argument("value")
            update_log_parser.add_argument("start_val")
            update_log_parser.add_argument("end_val")
            update_log_parser.add_argument("choice_list")
            args = update_log_parser.parse_args()

            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()

            tracker_timestamp_update = args.get('timestamp', None)
            note_update = args.get('note', None)

            if tracker.type == 'num':
                log = TRACKER_NUM.query.filter_by(log_id=log_id).first()

            elif tracker.type == 'bool':
                log = TRACKER_BOOL.query.filter_by(log_id=log_id).first()

            elif tracker.type == 'time_dur':
                log = TRACKER_TD.query.filter_by(log_id=log_id).first()

            elif tracker.type == 'mc':
                log = TRACKER_MC.query.filter_by(log_id=log_id).first()

                choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
                choices = choices_record.choices.split(",")
                choices_marked_record = TRACKER_MC.query.filter_by(log_id=log_id).first()
                choices_marked = choices_marked_record.value.split(",")

            # -----------

            if tracker.type == 'time_dur':
                tracker_value_start_update = args.get('start_val', None)
                tracker_value_end_update = args.get('end_val', None)

                log.time_start = tracker_value_start_update
                log.time_end = tracker_value_end_update
                log.note = note_update
                log.timestamp = tracker_timestamp_update
                db.session.commit()

            elif tracker.type == 'mc':
                tracker_values_update_list = args.get('choice_list')



                log.value = tracker_values_update_list
                log.timestamp = tracker_timestamp_update
                log.note = note_update
                db.session.commit()
                db.session.commit()

            else:
                tracker_value_update = args.get('value')

                log.value = tracker_value_update
                log.timestamp = tracker_timestamp_update
                log.note = note_update
                db.session.commit()

            return {"Update": "Successful"}

        else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
            return {"Message": "Login required."}, 400

    @jwt_required()
    def delete(self, tracker_id, log_id):

        si_un = get_jwt_identity()

        # If delete request, delete all cache
        cache.delete_memoized(getDashboardDetails, si_un)
        cache.delete_memoized(getTrackerDetails, si_un)
        cache.delete_memoized(getLogDetails, si_un, tracker_id)
        cache.delete_memoized(getTrackerInfo, si_un, tracker_id)
        cache.delete_memoized(getLogInfo, si_un, tracker_id)
        if si_un:

            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
            if tracker.type == 'num':
                log = TRACKER_NUM.query.filter_by(log_id=log_id).delete()

            elif tracker.type == 'bool':
                log = TRACKER_BOOL.query.filter_by(log_id=log_id).delete()

            elif tracker.type == 'time_dur':
                log = TRACKER_TD.query.filter_by(log_id=log_id).delete()

            elif tracker.type == 'mc':
                log = TRACKER_MC.query.filter_by(log_id=log_id).delete()

            db.session.commit()

            return {"Delete": "Successful"}

        else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
            return {"Message": "Login required."}, 400


class trackerInfoAPI(Resource):
    @jwt_required()
    def get(self, tracker_id):
        si_un = get_jwt_identity()
        results = getTrackerInfo(si_un, tracker_id)  # Cached results
        return results


class logInfoAPI(Resource):
    @jwt_required()
    def get(self, tracker_id, log_id):
        si_un = get_jwt_identity()
        results = getLogInfo(si_un, tracker_id, log_id)
        return results


# ----------------------
# to reset the password
# ----------------------
class ResetPass(Resource):
    def get(self):
        return {"msg": "working"}

    def post(self):
        forgetPass = reqparse.RequestParser()
        forgetPass.add_argument("username")
        args = forgetPass.parse_args()

        username = args.get("username", None).lower()

        forgotPassTASK.delay(username)

        return {"msg": "Done"}, 200



