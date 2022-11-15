import time
from flask import current_app as app, url_for
from .models import *
from .controller_index import *
from .controller_dash import *
from .graph import *
from .timestamp import *
from .to_csv import *
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from .celery_tasks import *
from .cache_instance import current_cache_inst as cache
from jinja2 import Template

'''
This particular .py file contains the api calls without using resources.
Here, we can find various sorts of Async tasks that can be called, ofc, asynchronously.

'''


# ----------------------
# to download logs
# ----------------------


@app.route("/api/<int:tracker_id>/details/download/")
@jwt_required()
@cache.memoize(timeout=25)  # So that the user doesn't spam the download button
def logDownload(tracker_id):
    username = get_jwt_identity()
    download_logsTASK.delay(tracker_id, username)
    return {'msg': "Done"}, 200


# ----------------------
# to download trackers
# ----------------------
@app.route("/api/trackers/download/")
@jwt_required()
@cache.memoize(timeout=25)  # So that the user doesn't spam the download button
def trackersDownload():
    si_un = get_jwt_identity()
    trackers = USER_TRACKER.query.filter_by(username=si_un)
    trackers_list = []
    for i in trackers:
        trackers_list.append(i.tracker_id)

    download_trackersTASK.delay(trackers_list, si_un)

    return {'msg': "Done"}, 200

