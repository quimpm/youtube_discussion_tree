import pickle
from datetime import datetime
import time

def get_current_quota():
    quota_controler = pickle.load(open(".quota.pickle", "rb"))
    return quota_controler.curr_quota

def actualize_current_quota(quota_operation):
    quota_controler = pickle.load(open(".quota.pickle", "rb"))
    curr_date = get_date(int(time.time()))
    if get_date(quota_controler.curr_date) != curr_date:
        quota_controler.curr_quota = quota_operation
        quota_controler.curr_date = curr_date
    else:
        quota_controler.curr_quota += quota_operation
    pickle.dump(quota_controler, open(".quota.pickle", "wb"))

def get_date(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')

def get_api_limit():
    return 10000