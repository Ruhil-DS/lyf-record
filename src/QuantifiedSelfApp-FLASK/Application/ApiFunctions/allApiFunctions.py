from flask_restful import Resource, reqparse
from flask import session, redirect, jsonify
from ..models import *
from ..timestamp import *
import datetime
from flask import request, redirect
from flask import session, url_for
from flask import current_app as app
from ..controller_index import *
from ..graph import *
from ..to_csv import *
import matplotlib.pyplot as plt
import os
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from ..cache_instance import current_cache_inst as cache

'''
This file contains all the cached functions which are to be used for the API
'''


@cache.memoize(timeout=120)
def getDashboardDetails(si_un=None):
    if si_un:

        streak = STREAK.query.filter_by(username=si_un).first().count
        # ----------------------

        # Tracker count ->
        trackers = USER_TRACKER.query.filter_by(username=si_un).distinct()
        tracker_count = 0
        for i in trackers:
            tracker_count += 1
        # ----------------------

        # member since ->
        member_create = USER.query.filter_by(username=si_un).first()
        member_since = str(
            datetime.datetime.today() - datetime.datetime.strptime(member_create.creation, '%Y-%m-%d'))
        member_since = member_since.split(",")
        member_since = member_since[0]
        # ----------------------

        # List of trackers ->
        tracker_ids = USER_TRACKER.query.filter_by(username=si_un).distinct()
        trackers = {}

        for t_id in tracker_ids:
            temp = (TRACKER.query.filter_by(tracker_id=t_id.tracker_id).first())
            trackers[temp.tracker_id] = [temp.name, temp.type, temp.last_log]

        # ----------------------

        #  path link for dashboard graph

        filename_path = plot_homepage(si_un=si_un)

        return jsonify(
            {"streak": streak, "tracker_count": tracker_count, "member_since": member_since, "trackers": trackers,
             "graph_path": filename_path})

    else:
        return {}, 404


@cache.memoize(timeout=120)
def getTrackerDetails(si_un=None):
    if si_un:

        tracker_ids = USER_TRACKER.query.filter_by(username=si_un).distinct()
        trackers = []
        for tid in tracker_ids:
            trackers.append(TRACKER.query.filter_by(tracker_id=tid.tracker_id).first())

        temp = {}
        for tracker in trackers:
            temp[tracker.tracker_id] = [tracker.name, tracker.description, tracker.type, tracker.last_log]
        return temp

    else:
        return {"message": "login required"}, "404"


@cache.memoize(timeout=120)
def getLogDetails(si_un=None, tracker_id=None):
    if si_un:

        try:
            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()

            if tracker.type == 'num':
                logs = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).all()
                filename_path = plot_numTracker(tracker_id, logs)

            elif tracker.type == 'bool':
                logs = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).all()
                filename_path = plot_BoolTracker(tracker_id, logs)

            elif tracker.type == 'time_dur':
                logs = TRACKER_TD.query.filter_by(tracker_id=tracker_id).all()
                filename_path = plot_tdTracker(tracker_id, logs)

            elif tracker.type == 'mc':
                logs = TRACKER_MC.query.filter_by(tracker_id=tracker_id).all()
                filename_path = plot_mcTracker(tracker_id, logs)

            temp = {"plot": filename_path, "type": tracker.type,
                    "logs": {}, "name": tracker.name}
            for log in logs:
                if tracker.type == 'time_dur':
                    temp["logs"][log.log_id] = [log.timestamp,
                                                [log.time_start, log.time_end],
                                                log.note]
                else:
                    temp["logs"][log.log_id] = [log.timestamp,
                                                log.value,
                                                log.note]

            return temp

        except:
            return {"Message": "Failed to retrieve data."}, 404

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return {"message": "Login required."}, 400


@cache.memoize(timeout=120)
def getTrackerInfo(si_un=None, tracker_id=None):
    if si_un:
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
        choices = None
        if tracker.type == 'mc':
            choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
            choices = choices_record.choices.split(",")

        data = {
            "name": tracker.name,
            "desc": tracker.description,
            "type": tracker.type,
            "choices": choices,
            "currentTime": str(current_timestamp())
        }

        return data, 200
    else:
        return {"msg": "Failed"}, 400


@cache.memoize(timeout=120)
def getLogInfo(si_un=None, tracker_id=None, log_id=None):
    if si_un:
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()

        if tracker.type == 'num':
            log = TRACKER_NUM.query.filter_by(log_id=log_id).first()

        elif tracker.type == 'bool':
            log = TRACKER_BOOL.query.filter_by(log_id=log_id).first()

        elif tracker.type == 'time_dur':
            log = TRACKER_TD.query.filter_by(log_id=log_id).first()

            data = {
                "trackerType": tracker.type,
                "trackerName": tracker.name,
                "start_time": log.time_start,
                "end_time": log.time_end,
                "timestamp": log.timestamp,
                "note": log.note,
            }
            return data, 200

        elif tracker.type == 'mc':
            log = TRACKER_MC.query.filter_by(log_id=log_id).first()

            choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
            choices = choices_record.choices.split(",")
            choices_marked_record = TRACKER_MC.query.filter_by(log_id=log_id).first()
            choices_marked = choices_marked_record.value.split(",")

            data = {
                "trackerType": tracker.type,
                "trackerName": tracker.name,
                "logValue": log.value,
                "timestamp": log.timestamp,
                "note": log.note,
                "choices": choices,
                "choicesMarked": choices_marked
            }

            return data, 200

        data = {
            "trackerName": tracker.name,
            "trackerType": tracker.type,
            "logValue": log.value,
            "timestamp": log.timestamp,
            "note": log.note,
        }

        return data, 200

    return {"msg": "Failed"}, 400